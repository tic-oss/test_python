from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.keycloak import oauth2_scheme
from schemas import schema
from models import models
from routers.router_utils import *
import logging


logger = logging.getLogger(__name__)


async def get_notes(db: Session = Depends(get_db)):
    logger.info("Received request to fetch notes")
    try:
       notes = db.query(models.Note).all()
       logger.info("Request to get all notes")
       return  notes
    except Exception as e:
        logger.error("An error occurred while fetching notes: %s", e)
        raise


async def create_note(note_note:schema.CreateNote, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    logger.info(f"Received request to create note: {note_note.dict()}")
    try:
       new_note = models.Note(**note_note.dict())
       db.add(new_note)
       db.commit()
       db.refresh(new_note)
   
       logger.info(f"New note Created Successfully with ID: {new_note.id}")
      
       message_to_publish = note_note.dict()
       await publish_message_to_queue(message_to_publish)
       return [new_note]
    
    except Exception as e:
        logger.error("An error occurred while processing the request: %s", e)
        raise


async def get_note(id:int ,db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    logger.info(f"Received request to fetch note with id: {id}")

    idv_note = db.query(models.Note).filter(models.Note.id == id).first()

    if idv_note is None:
        handle_invalid_note_id(id)
    logger.info(f"Request to get post by Id: {id}")    
    return idv_note


async def delete_note(id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    deleted_note = db.query(models.Note).filter(models.Note.id == id)
    logger.info(f"Received request to delete note with id: {id}")

    if deleted_note.first() is None:
        handle_invalid_note_id(id)
    deleted_note.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Note with id: {id} deleted successfully")



async def update_note(updated_note:schema.NoteBase, id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    logger.info(f"Received request to update note with id: {id}")
    updated_note =  db.query(models.Note).filter(models.Note.id == id).first()
   
    if updated_note.first() is None:
        handle_note_not_found(id)
    note_data = updated_note.dict()
    for field, value in note_data.item():
        setattr(updated_note, field, value)
    db.commit()
    logger.info(f"Note with id: {id} updated successfully")
    return  updated_note




