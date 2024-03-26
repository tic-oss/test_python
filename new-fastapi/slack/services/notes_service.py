from core.database import NOTES, DB
from pymongo import MongoClient
from bson import ObjectId
from models.models import Note
from routers.router_utils import *
import logging
import os


MONGO_URI = os.getenv("MONGO_URI")

Mongo_uri = MONGO_URI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)

def get_mongo_client():
    return MongoClient(MONGO_URI)


def get_notes():
    logger.info("Received request to fetch notes")
    try:
        with get_mongo_client() as client:
            notes = client[DB][NOTES]
            notes_list = notes.distinct()
            logger.info("Database connection successful")
            logger.info("Notes fetched successfully")
            return notes_list
    except Exception as e:
        logger.error("An error occurred while fetching notes: %s", e)
        raise


def get_note_id(id: int):
    logger.info(f"Received request to fetch note with id: {id}")
    with get_mongo_client() as client:
        notes = client[DB][NOTES]
        notes_list = notes.find({"id": id})
        response_notes_list = []
        for notes in notes_list:
            response_notes_list.append(Note(**notes))
        
        return response_notes_list

def post_notes(notes: Note):
    logger.info(f"Received request to create note: {notes.dict()}")
    with get_mongo_client() as client:
        notes = client[DB][NOTES]
        result = notes.insert_one(notes.dict())
        ack = result.acknowledged

        logger.info(f"New note added to the database with ID: {notes.id}")     
        
        return {"insertion": ack}



def update_notes(note_id: int, updated_notes: Note):

    logger.info(f"Received request to delete note with id: {id}")
    with get_mongo_client() as client:
        notes = client[DB][NOTES]
        result = notes.update_one({"_id": ObjectId(note_id)}, {"$set": updated_notes.dict()})
        
        if result.modified_count == 1:
            logger.info(f"Note with id: {id} updated successfully")
            return {"notes": "Update successful"}
        else:
            handle_note_not_found(id)

async def delete_notes(note_id: int):
   
    logger.info(f"Received request to update note with id: {id}")
    with get_mongo_client() as client:
        notes = client[DB][NOTES]
        result = notes.delete_one({"_id": ObjectId(note_id)})
        
        if result.deleted_count == 1:
            logger.info(f"Note with id: {id} deleted successfully")
            return {"notes": "Deletion successful"}
        else:
           handle_invalid_note_id(id)
    