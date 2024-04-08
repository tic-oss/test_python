import os
from pymongo import MongoClient

DB =  os.getenv("MONGO_DB")
MSG_COLLECTION = os.getenv("MONGO_MSG_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")

def get_mongo_client():
    return MongoClient(MONGO_URI)