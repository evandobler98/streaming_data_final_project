# Real-Time Baseball Streaming with Kafka

## Overview
This project simulates real-time baseball game updates using Apache Kafka. The producer generates live baseball events (e.g., hits, home runs, strikeouts) and streams them to a Kafka topic called "baseball-updates". The consumer listens to this topic, processes game events, and visualizes them using a dynamic scoreboard.

At the end of each game, the consumer announces the winner and resets for the next match.

## Dependencies

### 1. Install Python Virtual Environment
A virtual environment isolates dependencies for this project.

```bash
# Create virtual environment
python3 -m venv .venv  

# Activate virtual environment
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
2. Install Required Packages
Run the following command to install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Setting Up Kafka Locally
1. Start Zookeeper & Kafka
If Kafka is not already running, start Zookeeper and Kafka using two terminals.

Windows (PowerShell)
bash
Copy
Edit
# Terminal 1 - Start Zookeeper
zookeeper-server-start.bat config\zookeeper.properties

# Terminal 2 - Start Kafka
kafka-server-start.bat config\server.properties
macOS/Linux
bash
Copy
Edit
# Terminal 1 - Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Terminal 2 - Start Kafka
bin/kafka-server-start.sh config/server.properties
Running the Producer & Consumer
1. Start the Producer (Sends Baseball Events)
The producer generates live baseball game updates and publishes them to Kafka.

Windows
bash
Copy
Edit
.venv\Scripts\activate
py -m producers.baseball_producer
macOS/Linux
bash
Copy
Edit
source .venv/bin/activate
python3 -m producers.baseball_producer
2. Start the Consumer (Reads & Visualizes Games)
The consumer listens to the "baseball-updates" Kafka topic, processes game events, and updates a real-time scoreboard.

Windows
bash
Copy
Edit
.venv\Scripts\activate
py -m consumers.baseball_consumer
macOS/Linux
bash
Copy
Edit
source .venv/bin/activate
python3 -m consumers.baseball_consumer
Project Features
✔ Real-time Data Streaming: Producer sends live game updates to Kafka.
✔ Dynamic Scoreboard: Consumer updates the scoreboard as the game progresses.
✔ Automatic Game Reset: The system resets after each game and starts a new match.
✔ Kafka Integration: The project demonstrates how to work with Kafka topics for event-driven applications.

Troubleshooting
Kafka Not Working?
Run kafka-topics.sh --list --bootstrap-server localhost:9092 to verify Kafka is running.
Check if Zookeeper is running (ps aux | grep zookeeper).
Restart Kafka services and try again.
Consumer Not Receiving Messages?
Ensure the producer is running and sending messages.
Confirm the topic "baseball-updates" exists:
bash
Copy
Edit
kafka-topics.sh --describe --topic baseball-updates --bootstrap-server local