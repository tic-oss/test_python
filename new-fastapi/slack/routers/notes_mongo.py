from fastapi import  status, Depends, APIRouter
from core.keycloak import oauth2_scheme
from services.notes_service import *
from services import notes_service
from models.models import Note
from .router_utils import *
from typing import List

router = APIRouter(
    prefix='/api'
   
)

    
@router.get("/notes")
async def get_notes(token: str = Depends(oauth2_scheme)):
    return  await notes_service.get_notes()

@router.get("/notes/{id}", response_model=List[Note], status_code=status.HTTP_200_OK)
async def get_note_id(id: int, token: str = Depends(oauth2_scheme)):
    return  await notes_service.get_note_id(id, token)


@router.post("/notes", status_code=status.HTTP_201_CREATED)
async def post_note(notes: Note, token: str = Depends(oauth2_scheme)):

    ack = post_note(notes)
    logger.info(f"Received request to create note: {notes.dict()}")
    logger.info(f"New note created with ID: {notes.id}")
    return {"insertion": ack}


@router.put("/notes/{id}", status_code=status.HTTP_200_OK)
async def update_note(note_id: int, updated_notes: Note, token: str = Depends(oauth2_scheme)):

    if not update_note(note_id, updated_notes):
        handle_note_not_found()
    logger.info(f"Received request to update note with id: {id}")
    return {"message": "updated successfuly"}
   
        
@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, token: str = Depends(oauth2_scheme)):

    if not delete_note(note_id):
        handle_note_not_found()
    logger.info(f"Note with id: {id} deleted successfully")
    return {"message": "Deletion successfuly"}
   
    

    