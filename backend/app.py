from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from config import Config
from bson.json_util import dumps
from pymongo.mongo_client import MongoClient

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)

if mongo.cx:
    print("MongoDB connected successfully")
else:
    print("Failed to connect to MongoDB")


@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API is working!"}), 200
# @app.route('/api/test', methods=['GET'])
# def test_connection():
#     try:
#         mongo.db.test_collection.insert_one({'test': 'data'})
#         return {"status": "Connected and working!"}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500

# Endpoint to create a transaction
@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    print("Received data:", data)

    uri = "mongodb+srv://mohit2002:VZnPlg08gCI5krUB@mohitcluster.19qni.mongodb.net/?retryWrites=true&w=majority&appName=MohitCluster"
    client = MongoClient(uri)
    

    if data:
        try:
            db = client['demo'] 
            collection = db['data'] 
            # Attempt to insert data into the 'transactions' collection
            collection.insert_one(data)
            return {"message": "Transaction created successfully"}, 201
        except Exception as e:
            print("Error inserting data:", str(e))
            return {"error": str(e)}, 500
    else:
        return {"error": "No data provided"}, 400
    


# def create_transaction():
#     data = request.get_json()
#     transaction_id = data.get('transaction_id')
#     amount = data.get('amount')
#     timestamp = data.get('timestamp')
#     user_id = data.get('user_id')
#     transaction_type = data.get('transaction_type')
#     description = data.get('description')
#     status = data.get('status')
    
#     # Insert the transaction into the MongoDB collection
#     mongo.db.transactions.insert_one({
#         "transaction_id": transaction_id,
#         "amount": amount,
#         "timestamp": timestamp,
#         "user_id": user_id,
#         "transaction_type": transaction_type,
#         "description": description,
#         "status": status
#     })
    
    # return jsonify({"message": "Transaction created successfully!"}), 201

# Endpoint to get all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = mongo.db.transactions.find()
    return dumps(transactions)

# Endpoint to get a specific transaction by ID
@app.route('/api/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = mongo.db.transactions.find_one({"transaction_id": transaction_id})
    if transaction:
        return dumps(transaction)
    return jsonify({"error": "Transaction not found!"}), 404

# Endpoint to update a transaction by ID
@app.route('/api/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    mongo.db.transactions.update_one({"transaction_id": transaction_id}, {"$set": data})
    return jsonify({"message": "Transaction updated successfully!"})

# Endpoint to delete a transaction by ID
@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    result = mongo.db.transactions.delete_one({"transaction_id": transaction_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Transaction deleted successfully!"})
    return jsonify({"error": "Transaction not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
