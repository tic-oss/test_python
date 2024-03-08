from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
from backend.database import MSG_COLLECTION, DB
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

def get_channels_from_db():
    with get_mongo_client() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        distinct_channel_list = msg_collection.distinct("channel")
        return distinct_channel_list

def get_messages_from_db(channel: str):
    with get_mongo_client() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        msg_list = msg_collection.find({"channel": channel})
        response_msg_list = []
        for msg in msg_list:
            response_msg_list.append(Message(**msg))

        return response_msg_list

def insert_message_to_db(message: Message):
    with get_mongo_client() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(message.dict())
        ack = result.acknowledged
        return ack

def update_message_in_db(message_id: str, updated_message: Message):
    with get_mongo_client() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.update_one({"_id": ObjectId(message_id)}, {"$set": updated_message.dict()})
        return result.modified_count == 1

def delete_message_from_db(message_id: str):
    with get_mongo_client() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.delete_one({"_id": ObjectId(message_id)})
        return result.deleted_count == 1
