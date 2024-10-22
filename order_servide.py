import sqlite3
import time
from kafka import KafkaConsumer
from kafka_utils import create_kafka_consumer

DB_NAME = 'orders.db'

def init_order_db():
    """Inicializa la base de datos de pedidos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_order_to_db(product_id, status='PENDING'):
    """Guarda un pedido en la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (product_id, status) VALUES (?, ?)", (product_id, status))
    conn.commit()
    conn.close()

def process_orders():
    """Procesa los productos recibidos desde Kafka y crea pedidos."""
    consumer = create_kafka_consumer('productos')

    print("Esperando productos en el tema 'productos'...")
    for message in consumer:
        product = message.value
        print(f"Recibido producto: {product['title']} (ID: {product['id']})")

        # Simula un proceso complejo con una espera
        time.sleep(2)

        # Guarda el pedido en la base de datos
        save_order_to_db(product['id'], status='COMPLETED')
        print(f"Pedido creado para el producto {product['title']}.")

if __name__ == "__main__":
    init_order_db()  # Inicializa la base de datos
    process_orders()  # Procesa los pedidos
