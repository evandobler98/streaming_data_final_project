from kafka import KafkaProducer
import json
import time
import random
import sqlite3

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# SQLite Database Connection
conn = sqlite3.connect("games.db")
cursor = conn.cursor()

# Create a table to store baseball game events
cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game TEXT,
        inning INTEGER,
        score TEXT,
        player TEXT,
        event TEXT,
        timestamp REAL
    )
""")
conn.commit()

# Sample teams and players
teams = ["Yankees", "Red Sox", "Dodgers", "Rangers", "Mets", "Cubs"]
players = ["M. Trout", "C. Seager", "A. Judge", "B. Witt Jr.", "S. Ohtani"]

def generate_game_update(game_state):
    """Simulate a real-time baseball game update."""
    team1, team2 = game_state["teams"]
    
    if team1 == team2:
        return None  # Prevent self-matchups
    
    inning = game_state["inning"]
    player = random.choice(players)
    event = random.choice(["Hit", "Strikeout", "Walk", "Home Run", "Double"])

    # Update scores
    runs = game_state["score"].split('-')
    team1_score, team2_score = map(int, runs)

    if event in ["Hit", "Double"]:
        score_increase = random.randint(0, 3)
        if random.choice([True, False]):
            team1_score += score_increase
        else:
            team2_score += score_increase
    elif event == "Walk":
        if random.choice([True, False]):
            team1_score += 1
        else:
            team2_score += 1
    elif event == "Home Run":
        score_increase = random.randint(1, 4)
        if random.choice([True, False]):
            team1_score += score_increase
        else:
            team2_score += score_increase

    updated_score = f"{team1_score}-{team2_score}"
    game_state["score"] = updated_score

    event_data = {
        "game": f"{team1} vs {team2}",
        "inning": inning,
        "score": updated_score,
        "player": player,
        "event": event,
        "timestamp": time.time()
    }

    # Store event in SQLite
    cursor.execute("""
        INSERT INTO games (game, inning, score, player, event, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (event_data["game"], event_data["inning"], event_data["score"], event_data["player"], event_data["event"], event_data["timestamp"]))
    
    conn.commit()

    return event_data

def initialize_game():
    """Initialize a new game with a random matchup and score."""
    team1, team2 = random.sample(teams, 2)
    return {"teams": [team1, team2], "inning": 1, "score": "0-0"}

if __name__ == "__main__":
    print("Starting Baseball Producer...")

    while True:
        game_state = initialize_game()

        while game_state["inning"] <= 9:
            update = generate_game_update(game_state)
            if update:
                producer.send("baseball-updates", update)
                print(f"Produced: {update}")

            game_state["inning"] += 1
            time.sleep(2)

        print(f"Game {game_state['teams'][0]} vs {game_state['teams'][1]} completed!")
        time.sleep(5)
