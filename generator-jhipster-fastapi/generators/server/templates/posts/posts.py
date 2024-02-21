from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from db.postgres.database import get_db
from typing import List
from auth.keycloak import oauth2_scheme
from rabbitmq.producer import RabbitMQProducer
from rabbitmq.consumer import RabbitMQConsumer
from . import models
from . import schema
import threading
import logging


producer = RabbitMQProducer(queue_name="postsqueue")
consumer = RabbitMQConsumer(queue_name="slackqueue")
         
consumer_thread = threading.Thread(target=consumer.start_consuming, args=(consumer.queue_name,))
consumer_thread.start()  

logger = logging.getLogger(__name__)

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


<%_ if (db == "Mongo") { _%>                                       
from fastapi import  status, Depends, HTTPException, APIRouter
from pymongo import MongoClient
from typing import List
from auth.keycloak import oauth2_scheme
from db.mongo.database import MSG_COLLECTION, DB
from db.mongo.models import Message
from rabbitmq.producer import RabbitMQProducer
from rabbitmq.consumer import RabbitMQConsumer
import threading
import logging
from dotenv import load_dotenv
import os


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SLACK_PORT= os.getenv("POST_PORT")

producer = RabbitMQProducer(queue_name="pro_queue")
consumer = RabbitMQConsumer(queue_name="con_queue")

Mongo_uri = MONGO_URI

consumer_thread = threading.Thread(target=consumer.start_consuming, args=(consumer.queue_name,))
consumer_thread.start()   

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/slack',
    tags=['slack']

)


@router.get("/status")
async def get_status(token: str = Depends(oauth2_scheme)):
    """Get status of messaging server."""
    logger.info(f"request / endpoint!")
    return {"status": "running"}


@router.get("/channels", response_model=List[str])
async def get_channels(token: str = Depends(oauth2_scheme)):
    """Get all channels in list form."""
    logger.info(f"request / endpoint!")
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        distinct_channel_list = msg_collection.distinct("channel")
        logger.info(f"request / endpoint!")
        return distinct_channel_list


@router.get("/messages/{channel}", response_model=List[Message])
async def get_messages(channel: str, token: str = Depends(oauth2_scheme)):
    logger.info(f"request / endpoint!")
    """Get all messages for the specified channel."""
    with MongoClient(Mongo_uri) as client:
        msg_collection = client[DB][MSG_COLLECTION]
        msg_list = msg_collection.find({"channel": channel})
        response_msg_list = []
        for msg in msg_list:
            response_msg_list.append(Message(**msg))
        
        return response_msg_list


@router.post("/post_message", status_code=status.HTTP_201_CREATED)
async def post_message(message: Message, token: str = Depends(oauth2_scheme)):
    """Post a new message to the specified channel."""
    
    with MongoClient(Mongo_uri) as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(message.dict())
        ack = result.acknowledged

        logger.info(f"request / endpoint!")

        message_to_publish = message.dict()
        producer.publish_message(routing_key='pro_queue', message=message_to_publish)
        
        return {"insertion": ack}


@router.put("/update_message/{message_id}", status_code=status.HTTP_200_OK)
async def update_message(message_id: str, updated_message: Message, token: str = Depends(oauth2_scheme)):
    """Update an existing message with the specified ID."""
    logger.info(f"request / endpoint!")
    with MongoClient(Mongo_uri) as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.update_one({"_id": ObjectId(message_id)}, {"$set": updated_message.dict()})
        
        if result.modified_count == 1:
            return {"message": "Update successful"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        
@router.delete("/delete_message/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: str, token: str = Depends(oauth2_scheme)):
    """Delete a message with the specified ID."""
    logger.info(f"request / endpoint!")
    with MongoClient(Mongo_uri) as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.delete_one({"_id": ObjectId(message_id)})
        
        if result.deleted_count == 1:
            return {"message": "Deletion successful"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        
<%_ } _%>
    