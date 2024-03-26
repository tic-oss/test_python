from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from core.database import get_db
from typing import List
from core.keycloak import oauth2_scheme
from .router_utils import *
from models import models
from schemas.schema import NoteBase, CreateNote
from services import notes_service
import logging


router = APIRouter(
    prefix='/api'
)


@router.get('/notes', response_model=List[NoteBase], dependencies=[Depends(oauth2_scheme)])
async def get_notes(db: Session = Depends(get_db)):
    return  await notes_service.get_notes(db)
  
@router.post('/notes', status_code=status.HTTP_201_CREATED, response_model=NoteBase)
async def create_note(note_note:CreateNote, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_note = await notes_service.create_note(note_note, db, token)
    return new_note
    
@router.get('/notes/{id}', response_model=NoteBase, status_code=status.HTTP_200_OK)
async def get_note(id:int ,db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return  await notes_service.get_note(id, db, token)

@router.delete('/notes/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return  await notes_service.delete_note(id, db, token)

@router.put('/notes/{id}', response_model=CreateNote)
async def update_note(updated_note:NoteBase, id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return  await notes_service.update_note(updated_note, id, db, token)

  



