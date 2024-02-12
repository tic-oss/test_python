from fastapi import HTTPException, Depends, APIRouter, FastAPI
from sqlalchemy.orm import Session
from starlette import status
from .database import get_db
from typing import List, Union, Annotated
from pydantic import BaseModel
from .database import engine, Base
from .keycloak import oauth2_scheme
from rabbitmq.producer import RabbitMQProducer
from rabbitmq.consumer import RabbitMQConsumer
from . import models
from . import schema
import threading

producer = RabbitMQProducer("py_queue")
consumer = RabbitMQConsumer("py_queue")
         

consumer_thread = threading.Thread(target=consumer.start_consuming)
consumer_thread.start()  



router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)



@router.get('/', response_model=List[schema.CreatePost])
def test_posts(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    post = db.query(models.Post).all()
    return  post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schema.CreatePost])
def test_posts_sent(post_post:schema.CreatePost, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    new_post = models.Post(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    message_to_publish = post_post.dict()
    producer.publish_message(routing_key='py_queue', message=message_to_publish)
    
    return [new_post]


@router.get('/{id}', response_model=schema.CreatePost, status_code=status.HTTP_200_OK)
def get_test_one_post(id:int ,db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    idv_post = db.query(models.Post).filter(models.Post.id == id).first()

    if idv_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return idv_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_post(id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)


    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()



@router.put('/posts/{id}', response_model=schema.CreatePost)
def update_test_post(update_post:schema.PostBase, id:int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    updated_post =  db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()


    return  updated_post.first()