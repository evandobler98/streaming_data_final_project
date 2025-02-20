from kafka import KafkaProducer
import json
import time
import random

# Define the Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample teams
teams = ["Yankees", "Red Sox", "Dodgers", "Giants", "Mets", "Cubs"]

def generate_game_update():
    """Simulate a real-time baseball game update."""
    game = f"{random.choice(teams)} vs {random.choice(teams)}"
    score = f"{random.randint(0, 10)}-{random.randint(0, 10)}"
    return {"game": game, "score": score, "timestamp": time.time()}

if __name__ == "__main__":
    print("Starting Baseball Producer...")
    while True:
        update = generate_game_update()
        producer.send("baseball-updates", update)
        print(f"Produced: {update}")
        time.sleep(2)  # Simulate delay between updates
