from fastapi import  status, Depends, HTTPException, APIRouter
from pymongo import MongoClient
from typing import List
<%_ if (auth){  _%>
from services.keycloak import oauth2_scheme
<%_ } _%>
<%_ if (rabbitmqClient){  _%>
from services.rabbitmq.producer import RabbitMQProducer
<%_ } _%>
from backend.database import MSG_COLLECTION, DB
from models.models import Message
import threading
import logging
from dotenv import load_dotenv
import os


<%_ if (rabbitmqClient){  _%>
producer = RabbitMQProducer(exchange_name="direct_logs")
<%_ } _%>

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
PORT= os.getenv("PORT")


Mongo_uri = MONGO_URI


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/<%= baseName %>',
    tags=['<%= baseName %>']

)


@router.get("/status")
<%_ if (auth){  _%>
async def get_status(token: str = Depends(oauth2_scheme)):
<%_ } _%>
async def get_status():
    """Get status of messaging server."""
    logger.info(f"request / endpoint!")
    return {"status": "running"}


@router.get("/channels", response_model=List[str])
<%_ if (auth){  _%>
async def get_channels(token: str = Depends(oauth2_scheme)):
<%_ } _%>
async def get_channels():
    """Get all channels in list form."""
    logger.info(f"request / endpoint!")
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        distinct_channel_list = msg_collection.distinct("channel")
        logger.info(f"request / endpoint!")
        return distinct_channel_list


@router.get("/messages/{channel}", response_model=List[Message])
<%_ if (auth){  _%>
async def get_messages(channel: str, token: str = Depends(oauth2_scheme)):
<%_ } _%>
async def get_messages(channel: str):
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
<%_ if (auth){  _%>
async def post_message(message: Message, token: str = Depends(oauth2_scheme)):
<%_ } _%>
async def post_message(message: Message):
    """Post a new message to the specified channel."""
    
    with MongoClient(Mongo_uri) as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(message.dict())
        ack = result.acknowledged

        logger.info(f"request / endpoint!")

        <%_ if (rabbitmqClient){  _%>  
        message_to_publish = post_post.dict()
        producer.publish_message(routing_key='pro_queue', message=message_to_publish)
        <%_ } _%>
        return {"insertion": ack}


@router.put("/update_message/{message_id}", status_code=status.HTTP_200_OK)
<%_ if (auth){  _%>
async def update_message(message_id: str, updated_message: Message, token: str = Depends(oauth2_scheme)):
<%_ } _%>
async def update_message(message_id: str, updated_message: Message):

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
<%_ if (auth){  _%>
async def delete_message(message_id: str, token: str = Depends(oauth2_scheme)):
<%_ } _%>
async def delete_message(message_id: str):
    """Delete a message with the specified ID."""
    logger.info(f"request / endpoint!")
    with MongoClient(Mongo_uri) as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.delete_one({"_id": ObjectId(message_id)})
        
        if result.deleted_count == 1:
            return {"message": "Deletion successful"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        

    