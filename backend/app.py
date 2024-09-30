from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from config import Config, uri, client
from bson.json_util import dumps
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from kafka import KafkaProducer
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)
mongo_uri = uri

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

if mongo.cx:
    print("MongoDB connected successfully")
else:
    print("Failed to connect to MongoDB")


@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API is working!"}), 200

# Endpoint to create a transaction
@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    print("Received data:", data)

    if data:
        try:
            # Send the transaction data to Kafka
            producer.send('real_time_data', data)
            print(f'Sent message to Kafka: {data}')
            return {"message": "Transaction sent to Kafka successfully"}, 201
        except Exception as e:
            print(f"Error sending data to Kafka: {e}")
            return {"error": str(e)}, 500
    else:
        return {"error": "No data provided"}, 400


# Get All Transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    client = MongoClient(mongo_uri)
    db = client['Transactions']
    collection = db['Records']

    try:
        # Fetch all transactions
        transactions = list(collection.find())
        transactions_json = dumps(transactions)  # Convert to JSON string
        return transactions_json, 200
    except Exception as e:
        print("Error fetching transactions:", str(e))
        return {"error": str(e)}, 500


# Get a Single Transaction by ID
@app.route('/api/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    client = MongoClient(mongo_uri)
    db = client['Transactions']
    collection = db['Records']

    try:
        # Fetch transaction by 'transaction_id' (not _id)
        transaction = collection.find_one({"transaction_id": transaction_id})
        if transaction:
            transaction_json = dumps(transaction)
            return transaction_json, 200
        else:
            return {"error": "Transaction not found"}, 404
    except Exception as e:
        print("Error fetching transaction:", str(e))
        return {"error": str(e)}, 500

# Update a Transaction
@app.route('/api/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    client = MongoClient(mongo_uri)
    db = client['Transactions']
    collection = db['Records']

    if data:
        try:
            # Update transaction in MongoDB
            updated_transaction = collection.update_one(
                {"transaction_id": transaction_id},
                {"$set": data}
            )
            if updated_transaction.matched_count > 0:
                # Send the updated transaction data to Kafka
                producer.send('real_time_data', data)
                producer.flush()
                print(f'Sent updated transaction to Kafka: {data}')
                return {"message": "Transaction updated successfully and sent to Kafka"}, 200
            else:
                return {"error": "Transaction not found"}, 404
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return {"error": str(e)}, 500
    else:
        return {"error": "No data provided"}, 400

# Delete a Transaction
@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    data = request.get_json()
    client = MongoClient(mongo_uri)
    db = client['Transactions']
    collection = db['Records']
    
    try:
        # Delete transaction from MongoDB
        result = collection.delete_one({"transaction_id": transaction_id})
        if result.deleted_count > 0:
            # Send a delete message to Kafka
            delete_message = {
                "transaction_id": transaction_id,
                "message": "Transaction deleted"
            }
            producer.send('real_time_data', delete_message)
            producer.flush()
            print(f'Sent delete message to Kafka: {delete_message}')
            return {"message": "Transaction deleted and message sent to Kafka"}, 200
        else:
            return {"error": "Transaction not found"}, 404
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
