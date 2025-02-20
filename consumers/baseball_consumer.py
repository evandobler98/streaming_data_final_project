from kafka import KafkaConsumer
import json

# Define Kafka consumer
consumer = KafkaConsumer(
    "baseball-updates",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Starting Baseball Consumer...")
for message in consumer:
    data = message.value
    print(f"Consumed: {data}")
