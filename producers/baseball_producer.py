from kafka import KafkaProducer
import json
import time
import random

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample teams and players
teams = ["Yankees", "Red Sox", "Dodgers", "Rangers", "Mets", "Cubs"]
players = ["M. Trout", "C. Seager", "A. Judge", "B. Witt Jr.", "S. Ohtani"]

def generate_game_update(game_state):
    """Simulate a real-time baseball game update."""
    team1, team2 = game_state["teams"]
    
    if team1 == team2:
        return None  # Ensure a team isn't playing against itself
    
    inning = game_state["inning"]
    player = random.choice(players)
    event = random.choice(["Hit", "Strikeout", "Walk", "Home Run", "Double"])

    # Simulate a score change based on the event
    runs = game_state["score"].split('-')
    team1_score = int(runs[0])
    team2_score = int(runs[1])

    # Handle the event and update the score
    if event == "Hit" or event == "Double":
        # Randomly increase score by 0 to 3
        score_increase = random.randint(0, 3)
        if random.choice([True, False]):  # Randomly assign score increase to one of the teams
            team1_score += score_increase
        else:
            team2_score += score_increase
    elif event == "Walk":
        # Increase score by 0 or 1
        score_increase = random.choice([0, 1])
        if random.choice([True, False]):
            team1_score += score_increase
        else:
            team2_score += score_increase
    elif event == "Home Run":
        # Increase score by 1 to 4
        score_increase = random.randint(1, 4)
        if random.choice([True, False]):
            team1_score += score_increase
        else:
            team2_score += score_increase
    elif event == "Strikeout":
        # No score change for strikeout
        pass

    # Format updated score (accumulated score)
    updated_score = f"{team1_score}-{team2_score}"

    # Update the game state with the new score
    game_state["score"] = updated_score

    # Return update
    return {
        "game": f"{team1} vs {team2}",
        "inning": inning,
        "score": updated_score,
        "player": player,
        "event": event,
        "timestamp": time.time()
    }

def initialize_game():
    """Initialize the game with a random match-up and score."""
    team1, team2 = random.sample(teams, 2)  # Ensure teams are different
    return {
        "teams": [team1, team2],
        "inning": 1,
        "score": "0-0"
    }

def handle_extra_innings(game_state, team1_score, team2_score):
    """Handle extra innings if the game is tied after 9 innings."""
    while team1_score == team2_score:
        game_state["inning"] += 1  # Start extra innings
        return generate_game_update(game_state)
    return None  # No extra inning logic needed if the game has a winner

if __name__ == "__main__":
    print("Starting Baseball Producer...")
    
    while True:
        # Initialize a new game after each one finishes
        game_state = initialize_game()

        # Simulate a game for at least 9 innings
        while game_state["inning"] <= 9:
            update = generate_game_update(game_state)
            
            if update:
                producer.send("baseball-updates", update)
                print(f"Produced: {update}")
            
            # Prepare for the next inning
            game_state["inning"] += 1
            time.sleep(2)  # Simulate delay between updates

        # Handle extra innings if the game is tied
        team1_score, team2_score = map(int, game_state["score"].split('-'))
        if team1_score == team2_score:
            print(f"Game is tied after 9 innings. Going to extra innings.")
            while team1_score == team2_score:
                extra_inning_update = handle_extra_innings(game_state, team1_score, team2_score)
                if extra_inning_update:
                    producer.send("baseball-updates", extra_inning_update)
                    print(f"Produced: {extra_inning_update}")
                    team1_score, team2_score = map(int, extra_inning_update["score"].split('-'))
                    time.sleep(2)
        
        # Determine the winner
        winner = game_state["teams"][0] if team1_score > team2_score else game_state["teams"][1]
        print(f"Game {game_state['teams'][0]} vs {game_state['teams'][1]} completed! {winner} wins!")
        time.sleep(5)  # Optional: Delay before starting the next game
