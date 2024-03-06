from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from backend.database import get_db
from typing import List
from services.keycloak import oauth2_scheme
from services.rabbitmq.producer import RabbitMQProducer
from models import models
from schemas import schema

import logging
logger = logging.getLogger(__name__)

producer = RabbitMQProducer(exchange_name="direct_logs")


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)



@router.get('/', response_model=List[schema.CreatePost])
async def post(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    posts = db.query(models.Post).all()
    logger.info(f"request / endpoint!")
    return  posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schema.CreatePost])
async def posts_sent(post_post:schema.CreatePost, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    new_post = models.Post(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    logger.info(f"request / endpoint!")
       
    message_to_publish = post_post.dict()
    producer.publish_message(routing_key='pro_queue', message=message_to_publish)
   
    return [new_post]


@router.get('/{id}', response_model=schema.CreatePost, status_code=status.HTTP_200_OK)
async def get_one_post(id:int ,db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    idv_post = db.query(models.Post).filter(models.Post.id == id).first()

    if idv_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    logger.info(f"request / endpoint!")
    return idv_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)


    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    logger.info(f"request / endpoint!")


@router.put('/posts/{id}', response_model=schema.CreatePost)
async def update_post(update_post:schema.PostBase, id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    updated_post =  db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()
    logger.info(f"request / endpoint!")

    return  updated_post.first()