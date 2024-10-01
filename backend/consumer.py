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
analytics_collection = db['Analytics']  # Use Analytics collection

MAX_RETRIES = 5  # Number of retries for MongoDB insertion failures
RETRY_INTERVAL = 2  # Time to wait between retries (in seconds)

def consume_analytics(topic):
    """Consume aggregated messages from the Kafka analytics topic."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        group_id="analytics-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    try:
        print(f"Listening to analytics topic {topic}...")
        for message in consumer:
            analytics_data = message.value
            print(f"Received aggregated data: {analytics_data}")

            # Insert the analytics data into the MongoDB Analytics collection
            try:
                analytics_collection.insert_one(analytics_data)
                print(f"Aggregated data inserted into MongoDB Analytics collection.")
            except Exception as e:
                print(f"Failed to insert analytics data: {e}")

    except Exception as e:
        print(f"Failed to consume message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_analytics("transaction_analytics")
