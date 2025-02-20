from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    "baseball-updates",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Store cumulative scores for each game
game_scores = defaultdict(lambda: {"team1": 0, "team2": 0})

# Set up Matplotlib for Scoreboard
plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))

# Function to update the scoreboard
def update_scoreboard(game, score, inning):
    """Update the scoreboard visualization."""
    # Extract team names and scores
    team1, team2 = game.split(' vs ')
    team1_score, team2_score = map(int, score.split('-'))

    # Clear the plot and redraw the scoreboard
    ax.clear()

    # Set the title and labels for the plot
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Game: {team1} vs {team2} | Inning: {inning}", fontsize=16)

    # Draw the team names and their scores
    ax.text(2, 7, f"{team1}: {team1_score}", fontsize=20, ha='center', color='blue')
    ax.text(8, 7, f"{team2}: {team2_score}", fontsize=20, ha='center', color='red')

    # Display the inning in the middle
    ax.text(5, 3, f"Inning {inning}", fontsize=30, ha='center', color='black')

    plt.draw()
    plt.pause(0.5)

def display_winner(game, score):
    """Display the winner of the game."""
    team1_score, team2_score = map(int, score.split('-'))
    if team1_score > team2_score:
        winner = game.split(' vs ')[0]
    else:
        winner = game.split(' vs ')[1]
    
    print(f"Winner: {winner} wins the game!")

print("Starting Baseball Consumer...")
for message in consumer:
    data = message.value
    print(f"Consumed: {data}")

    # Update the cumulative scores for the game
    team1, team2 = data["game"].split(' vs ')
    team1_score, team2_score = map(int, data["score"].split('-'))
    game_scores[data["game"]]["team1"] = team1_score
    game_scores[data["game"]]["team2"] = team2_score

    # Update the scoreboard visualization with the new data
    update_scoreboard(data["game"], data["score"], data["inning"])

    # Display the winner after 9 innings
    if data["inning"] == 9:
        display_winner(data["game"], data["score"])
