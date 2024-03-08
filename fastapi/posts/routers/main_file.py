from fastapi import APIRouter, Depends
from typing import List
from starlette import status
from backend.database import get_db
from services.keycloak import oauth2_scheme
from .router_utils import *

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schema.PostBase], dependencies=[Depends(oauth2_scheme)]) 
async def get_posts_route(db: Session = Depends(get_db)):
    return await get_posts(db)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PostBase)
async def create_post_route(post_post: schema.CreatePost, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    new_post = await create_post(post_post, db, token)
    return new_post

@router.get('/{id}', response_model=schema.PostBase, status_code=status.HTTP_200_OK)
async def get_one_post_route(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await get_one_post(id, db, token)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_route(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    await delete_post(id, db, token)

@router.put('/{id}', response_model=schema.PostBase)
async def update_post_route(updated_post: schema.PostBase, id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await update_post(updated_post, id, db, token)
