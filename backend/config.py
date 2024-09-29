import os
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8077119512'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://mohit2002:VZnPlg08gCI5krUB@mohitcluster.19qni.mongodb.net/?retryWrites=true&w=majority&appName=MohitCluster'

uri = os.getenv("MONGO_URI")
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

