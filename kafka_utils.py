from kafka import KafkaProducer, KafkaConsumer
import json
import time

time.sleep(5)  # Esperar unos segundos para que Kafka esté disponible

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['host.docker.internal:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def create_kafka_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers=['host.docker.internal:9092'],  # Ajuste para Docker en Windows
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',  # Lee desde el principio del tema
        group_id='order-service'
    )