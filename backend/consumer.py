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
    """Consume messages from the Kafka topic and insert into MongoDB with error handling."""
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
            transaction_data = message.value
            print(f"Received message: {transaction_data}")

            # Check for existing transaction_id in MongoDB (deduplication)
            if collection.find_one({"transaction_id": transaction_data["transaction_id"]}):
                print(f"Transaction {transaction_data['transaction_id']} already exists in MongoDB. Skipping insertion.")
                continue

            # Attempt to insert the transaction data into MongoDB
            retry_count = 0
            while retry_count < MAX_RETRIES:
                try:
                    collection.insert_one(transaction_data)
                    print(f"Transaction {transaction_data['transaction_id']} inserted into MongoDB.")
                    break  # Break out of retry loop if successful
                except Exception as e:
                    print(f"Error inserting into MongoDB: {e}")
                    retry_count += 1
                    if retry_count < MAX_RETRIES:
                        print(f"Retrying ({retry_count}/{MAX_RETRIES}) in {RETRY_INTERVAL} seconds...")
                        time.sleep(RETRY_INTERVAL)
                    else:
                        print(f"Failed to insert transaction {transaction_data['transaction_id']} after {MAX_RETRIES} retries.")
    except Exception as e:
        print(f"Failed to consume message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages("real_time_data")