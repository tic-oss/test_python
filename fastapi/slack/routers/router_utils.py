from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
from core.database import MSG_COLLECTION, DB
from models.slack import Message
import logging
import os

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI")

def get_mongo_client():
    return MongoClient(MONGO_URI)

def handle_message_not_found():
    raise HTTPException(status_code=404, detail="Message not found")

def handle_channel_not_found():
    raise HTTPException(status_code=404, detail="Channel not found")

def handle_internal_server_error():
    raise HTTPException(status_code=500, detail="Internal server error")

