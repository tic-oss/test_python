from fastapi import HTTPException
from pymongo import MongoClient
import logging
import os

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI")

def get_mongo_client():
    return MongoClient(MONGO_URI)

def handle_note_not_found(id: int):
    raise HTTPException(status_code=404, detail=f"The id: {id} does not exist")
    
def handle_invalid_note_id(id: int):
    raise HTTPException(status_code=400, detail=f"The id: {id} you requested for does not exist")
    
def handle_internal_server_error():
    raise HTTPException(status_code=500, detail="Internal server error")