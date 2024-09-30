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
    send_financial_transaction("807711", 15500.50, "2024-09-18T12:00:00Z", "Dawid Warner", "Personal", "Personal Payment for Warner", "Success")
    time.sleep(5)  # Send a message every 5 seconds
