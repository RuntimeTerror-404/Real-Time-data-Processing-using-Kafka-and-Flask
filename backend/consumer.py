from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI") 
client = MongoClient(mongo_uri)
db = client['Transactions']  # Use Transactions database
collection = db['Records']    # Use Records collection

def consume_messages(topic):
    """Consume messages from the Kafka topic and insert into MongoDB."""
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
            
            # Check for existing transaction_id in MongoDB
            if collection.find_one({"transaction_id": transaction_data["transaction_id"]}):
                print(f"Transaction {transaction_data['transaction_id']} already exists in MongoDB. Skipping insertion.")
            else:
                # Insert received transaction data into MongoDB
                try:
                    collection.insert_one(transaction_data)
                    print(f"Transaction {transaction_data['transaction_id']} inserted into MongoDB.")
                except Exception as e:
                    print(f"Error inserting into MongoDB: {e}")
    except Exception as e:
        print(f"Failed to consume message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages("real_time_data")
