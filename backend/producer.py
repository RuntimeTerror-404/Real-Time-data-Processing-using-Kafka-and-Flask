import json
from kafka import KafkaProducer
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_financial_transaction(transaction_id, amount, timestamp, user_id, transaction_type, description, status):
    message = {
        "transaction_id": transaction_id,
        "amount": amount,
        "timestamp": timestamp,
        "user_id": user_id,
        "transaction_type": transaction_type,
        "description": description,
        "status": status
    }
    producer.send('real_time_data', message)
    print(f'Sent message: {message}')

# Example of sending a transaction
while True:
    send_financial_transaction("12345", 250.75, "2024-09-28T12:00:00Z", "user_001", "credit", "Payment for invoice #5678", "completed")
    time.sleep(5)  # Send a message every 5 seconds
