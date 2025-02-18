import json
import pathlib
import sys
import sqlite3
from kafka import KafkaConsumer
import utils.utils_config as config
from utils.utils_logger import logger
from utils.utils_producer import verify_services, is_topic_available

# Database initialization
def init_db(sql_path: pathlib.Path):
    """Initialize the SQLite database with the necessary table."""
    try:
        conn = sqlite3.connect(sql_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                author TEXT,
                timestamp TEXT,
                category TEXT,
                sentiment REAL,
                keyword_mentioned TEXT,
                message_length INTEGER
            )
            """
        )
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(3)
    finally:
        conn.close()

# Insert processed message into the database
def insert_message(message_data: dict, sql_path: pathlib.Path):
    """Insert a processed message into the database."""
    try:
        conn = sqlite3.connect(sql_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO processed_messages (message, author, timestamp, category, sentiment, keyword_mentioned, message_length)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message_data["message"],
                message_data["author"],
                message_data["timestamp"],
                message_data["category"],
                message_data["sentiment"],
                message_data["keyword_mentioned"],
                message_data["message_length"],
            ),
        )
        conn.commit()
        logger.info("Message stored successfully.")
    except Exception as e:
        logger.error(f"Error inserting message: {e}")
    finally:
        conn.close()

# Consume messages from Kafka
def consume_messages():
    """Consume messages from Kafka and process them."""
    try:
        topic = config.get_kafka_topic()
        kafka_url = config.get_kafka_broker_address()
        group_id = config.get_kafka_consumer_group_id()
        sql_path = config.get_sqlite_path()
        
        logger.info("Starting Kafka consumer...")
        verify_services()
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_url,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
        
        is_topic_available(topic)
        init_db(sql_path)
        
        for message in consumer:
            processed_message = message.value
            logger.info(f"Received message: {processed_message}")
            insert_message(processed_message, sql_path)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Consumer error: {e}")
    finally:
        logger.info("Consumer shutting down.")

if __name__ == "__main__":
    consume_messages()
