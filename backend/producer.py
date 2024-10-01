import json
from kafka import KafkaProducer
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_financial_transaction(transaction_id, amount, timestamp, user_id, transaction_type, description, status, organization):
    message = {
        "transaction_id": transaction_id,
        "amount": amount,
        "timestamp": timestamp,
        "user_id": user_id,
        "transaction_type": transaction_type,
        "description": description,
        "status": status,
        'organization': organization
    }
    producer.send('real_time_data', message)
    print(f'Sent message: {message}')

# Example of sending a transaction
while True:
    send_financial_transaction("000777", 44000.50, "2021-12-27T12:00:00Z", "Mohit P", "Personal", "Personal Payment for Warner", "Success", "American Express")
    time.sleep(5)  # Send a message every 5 seconds
