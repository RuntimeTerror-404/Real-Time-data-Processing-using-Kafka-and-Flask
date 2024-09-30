from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time

load_dotenv()

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI") 
client = MongoClient(mongo_uri)
db = client['Transactions']  # Use Transactions database
collection = db['Records']    # Use Records collection

MAX_RETRIES = 5  # Number of retries for MongoDB insertion failures
RETRY_INTERVAL = 2  # Time to wait between retries (in seconds)

def consume_messages(topic):
    """Consume messages from the Kafka topic."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        group_id="consumer-group-1",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    try:
        print(f"Listening to topic {topic}...")
        for message in consumer:
            message_value = message.value
            print(f"Received message: {message_value}")
            
            # Check if the message is a deletion notification
            if "message" in message_value and message_value["message"] == "Transaction deleted":
                print(f"Transaction {message_value['transaction_id']} deleted. No insertion needed.")
            else:
                # Insert the transaction into MongoDB if it's not a deletion notice
                collection.insert_one(message_value)
                print(f"Transaction {message_value['transaction_id']} inserted into MongoDB.")
                
    except Exception as e:
        print(f"Failed to consume message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages("real_time_data")