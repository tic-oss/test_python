from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.keycloak import oauth2_scheme
# from core.rabbitmq.producer import RabbitMQProducer
from schemas import post_schema
from models import post 
from routers.router_utils import *
import logging
logger = logging.getLogger(__name__)

async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(post.Post).all()
    logger.info("Request to get all posts")
    return posts


async def create_post(post_post: post_schema.CreatePost, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_post = post.Post(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    logger.info(f" Post Created Successfully !")
       
    message_to_publish = post_post.dict()
    await publish_message_to_queue(message_to_publish)
    return new_post


async def get_post(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    idv_post = db.query(post.Post).filter(post.Post.id == id).first()
    if idv_post is None:
        handle_invalid_post_id(id)
    logger.info(f"Request to get post by Id")
    return idv_post


async def delete_post(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    deleted_post = db.query(post.Post).filter(post.Post.id == id)
    if deleted_post.first() is None:
        handle_invalid_post_id(id)
    deleted_post.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Post Deleted Succesfully !")


async def update_post(updated_post: post_schema.PostBase, id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    post_to_update = db.query(post.Post).filter(post.Post.id == id).first()
    if post_to_update is None:
        handle_post_not_found(id)
    post_data = updated_post.dict()
    for field, value in post_data.items():
        setattr(post_to_update, field, value)
    db.commit()
    logger.info(f"{id} post Updated Successfully !")
    return post_to_update
