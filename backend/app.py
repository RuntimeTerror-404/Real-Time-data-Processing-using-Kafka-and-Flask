from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from config import Config, uri, client
from bson.json_util import dumps
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)
mongo_uri = uri

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

    client = MongoClient(mongo_uri)
    
    if data:
        try:
            # Create database named Transactions if they don't exist already
            db = client['Transactions'] 
            # Create collection named Records if it doesn't exist already 
            collection = db['Records'] 
            # Attempt to insert data into the 'transactions' collection
            collection.insert_one(data)
            return {"message": "Transaction created successfully"}, 201
        except Exception as e:
            print("Error inserting data:", str(e))
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
            # Update transaction by 'transaction_id'
            updated_transaction = collection.update_one(
                {"transaction_id": transaction_id},  # Match by transaction_id
                {"$set": data}  # Update fields with the data provided
            )
            
            if updated_transaction.matched_count > 0:
                return {"message": "Transaction updated successfully"}, 200
            else:
                return {"error": "Transaction not found"}, 404
        except Exception as e:
            print("Error updating transaction:", str(e))
            return {"error": str(e)}, 500
    else:
        return {"error": "No data provided"}, 400

# Delete a Transaction
@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    client = MongoClient(mongo_uri)
    db = client['Transactions']
    collection = db['Records']

    try:
        # Delete transaction by 'transaction_id'
        result = collection.delete_one({"transaction_id": transaction_id})
        
        if result.deleted_count > 0:
            return {"message": "Transaction deleted successfully"}, 200
        else:
            return {"error": "Transaction not found"}, 404
    except Exception as e:
        print("Error deleting transaction:", str(e))
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
