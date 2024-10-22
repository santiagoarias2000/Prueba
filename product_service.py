import requests
import sqlite3
import time
from kafka import KafkaProducer
import json
from kafka_utils import create_kafka_producer

DB_NAME = 'products.db'
KAFKA_TOPIC = 'productos'
DLQ_TOPIC = 'productos_dlq'
API_URL = "https://fakestoreapi.com/products"

# Inicializar productor Kafka
producer = create_kafka_producer()

def save_product_to_db(product):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (id, name, category, price) VALUES (?, ?, ?, ?)",
        (product['id'], product['title'], product['category'], product['price'])
    )
    conn.commit()
    conn.close()

def fetch_products_with_retries(retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            products = response.json()

            # Enviar productos a Kafka y guardarlos en SQLite
            for product in products:
                producer.send(KAFKA_TOPIC, product)
                save_product_to_db(product)

            print("Productos enviados a Kafka y guardados en SQLite.")
            return

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener productos: {e}. Reintentando...")
            time.sleep(delay * (2 ** attempt))  # Backoff exponencial

    # Si fallan todos los intentos, enviar a DLQ
    print("No se pudo obtener productos. Enviando a DLQ...")
    producer.send(DLQ_TOPIC, {"error": "No se pudo obtener productos después de varios intentos."})

if __name__ == "__main__":
    fetch_products_with_retries()
