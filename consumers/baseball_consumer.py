from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import time

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

# Team colors mapping
team_colors = {
    "Rangers": "lightblue",
    "Cubs": "royalblue",
    "Dodgers": "blue",
    "Yankees": "darkblue",
    "Red Sox": "red",
    "Mets": "orange"
}

# Function to update the scoreboard
def update_scoreboard(game, score, inning, player, event, winner=None):
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

    # Draw the team names and their scores with team colors
    ax.text(2, 7, f"{team1}: {team1_score}", fontsize=20, ha='center', color=team_colors[team1])
    ax.text(8, 7, f"{team2}: {team2_score}", fontsize=20, ha='center', color=team_colors[team2])

    # Display the inning in the middle
    ax.text(5, 3, f"Inning {inning}", fontsize=30, ha='center', color='black')

    # Display the player and event happening
    ax.text(5, 1, f"{player} - {event}", fontsize=16, ha='center', color='black')

    # Display the winner in big letters at the end of the game
    if winner:
        ax.text(5, 5, f"Winner: {winner}!", fontsize=50, ha='center', color='green', fontweight='bold')

    plt.draw()
    plt.pause(0.5)

def display_winner(game, score):
    """Determine and return the winner of the game."""
    team1_score, team2_score = map(int, score.split('-'))
    if team1_score > team2_score:
        winner = game.split(' vs ')[0]
    else:
        winner = game.split(' vs ')[1]
    return winner

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
    winner = None
    if data["inning"] == 9:  # If it's the 9th inning, check the winner
        winner = display_winner(data["game"], data["score"])

    # Update the scoreboard with the winner (if game is over) or current game info
    update_scoreboard(data["game"], data["score"], data["inning"], data["player"], data["event"], winner)

    # Display winner and stop the game after 9 innings
    if winner:
        print(f"Winner: {winner} wins the game!")
        time.sleep(5)  # Pause for 5 seconds to show the winner before the next game starts
