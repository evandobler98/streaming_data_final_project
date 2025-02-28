# Streaming Data Final Project

This project involves real-time streaming of baseball game updates using Kafka. My custom consumer listens to the "baseball-updates" Kafka topic, processes live baseball game events, and updates a dynamic scoreboard. The system maintains a cumulative score for each team, dynamically updates the scoreboard with team colors, inning progress, and real-time game events (such as home runs and strikeouts). At the end of each game, it declares the winner in bold and resets for the next match. Additionally, game data is stored in SQLite for future reference.

## Table of Contents

- [VS Code Extensions](#vs-code-extensions)
- [Task 1: Manage Local Project Virtual Environment](#task-1-manage-local-project-virtual-environment)
- [Task 2: Start Zookeeper and Kafka](#task-2-start-zookeeper-and-kafka-takes-2-terminals)
- [Task 3: Start a New Streaming Application](#task-3-start-a-new-streaming-application)
- [Save Space](#save-space)

## VS Code Extensions

Here are some useful VS Code extensions to enhance your experience:

- **Black Formatter** by Microsoft
- **Markdown All in One** by Yu Zhang
- **PowerShell** by Microsoft (for Windows users)
- **Pylance** by Microsoft
- **Python** by Microsoft
- **Python Debugger** by Microsoft
- **Ruff** by Astral Software (Linter)
- **SQLite Viewer** by Florian Klampfer
- **WSL** by Microsoft (for Windows users)

## Task 1: Manage Local Project Virtual Environment

To set up your virtual environment and install dependencies, follow these steps:

1. **Create the `.venv`**:
    ```bash
    python3 -m venv .venv
    ```

2. **Activate the virtual environment**:
    - On **Windows**:
        ```bash
        .venv\Scripts\activate
        ```
    - On **macOS/Linux**:
        ```bash
        source .venv/bin/activate
        ```

3. **Install the required dependencies** from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Task 2: Start Zookeeper and Kafka (Takes 2 Terminals)

If Zookeeper and Kafka are not already running, you need to restart them. Follow the instructions in the [SETUP-KAFKA.md](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md) file for setting them up:

1. **Start Zookeeper Service**  
   [Setup Instructions](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md#step-7-start-zookeeper-service-terminal-1)

2. **Start Kafka Service**  
   [Setup Instructions](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md#step-8-start-kafka-terminal-2)

## Task 3: Start a New Streaming Application

This requires two additional terminals: one for the producer (which writes messages) and one for the consumer (which reads, processes, and writes messages to a data store).

### Producer (Terminal 3)

Start the producer to generate live messages. The producer writes to a live data file in the `data` folder, and if Zookeeper and Kafka are running, it will also write to a Kafka topic.

To start the producer:

1. Open a **new terminal** in VS Code.
2. Activate the virtual environment and start the producer using the following commands:

#### Windows:
```shell
.venv\Scripts\activate
py -m producers.baseball_producer
```

#### macOS/Linux:
```source .venv/bin/activate
python3 -m producers.baseball_producer
```
Note: The producer will work even if Kafka is not available, but it will write to a data file instead of Kafka.

#### Consumer (Terminal 4) - Two Options

You have two options for the consumer:
1. **Consumer reading from the live data file**
2. **Consumer reading from the Kafka topic**

To start the consumer:
1. **Open a new terminal in your root project folder.**
Activate the virtual environment and choose the consumer option you'd like to use.
Windows:
```.venv\Scripts\activate
py -m consumers.baseball_consumer
```

macOS/Linux:
```source .venv/bin/activate
python3 -m consumers.baseball_consumer
```
Save Space
To save disk space when you're not actively working on the project:

Delete the .venv folder.
You can always recreate it later by following the steps to activate the virtual environment and reinstall the necessary packages.
