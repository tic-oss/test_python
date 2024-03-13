from fastapi import APIRouter, Depends
from typing import List
from requests import Session
from starlette import status
from core.database import get_db
from core.keycloak import oauth2_scheme
from .router_utils import *
from schemas.post_schema import PostBase,CreatePost
from services import post_service
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[PostBase], dependencies=[Depends(oauth2_scheme)]) 
async def get_posts(db: Session = Depends(get_db)):
    return await post_service.get_posts(db)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostBase)
async def create_post(post_post:CreatePost, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    new_post = await post_service.create_post(post_post, db, token)
    return new_post

@router.get('/{id}', response_model=PostBase, status_code=status.HTTP_200_OK)
async def get_post(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await post_service.get_post(id, db, token)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    await post_service.delete_post(id, db, token)

@router.put('/{id}', response_model=PostBase)
async def update_post(updated_post: PostBase, id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await post_service.update_post(updated_post, id, db, token)
