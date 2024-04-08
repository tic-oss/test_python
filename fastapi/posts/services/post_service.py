from fastapi import Depends
from core.database import get_db
from core.auth import *
from schemas import post_schema
from models import post 
from routers.router_utils import *
import logging

logger = logging.getLogger(__name__)

async def create_post(post_post: post_schema.CreatePost, token: str = Depends(get_auth)):
    db = next(get_db())
    new_post = post.Post(**post_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    logger.info(f" Post Created Successfully !")
    message_to_publish = post_post.model_dump()
    await publish_message_to_queue(message_to_publish)
    return new_post


async def get_posts(token: str = Depends(get_auth)):
    db = next(get_db())
    posts = db.query(post.Post).all()
    logger.info("Request to get all posts")
    return posts


async def get_post(id: int, token: str = Depends(get_auth)):
    db = next(get_db())
    idv_post = db.query(post.Post).filter(post.Post.id == id).first()
    if idv_post is None:
        handle_invalid_post_id(id)
    logger.info(f"Request to get post by Id")
    return idv_post
                                            

async def update_post(updated_post: post_schema.PostBase, id: int, token: str = Depends(get_auth)):
    db = next(get_db())
    post_to_update = db.query(post.Post).filter(post.Post.id == id).first()
    if post_to_update is None:
        handle_post_not_found(id)
    post_data = updated_post.model_dump()
    for field, value in post_data.items():
        setattr(post_to_update, field, value)
    db.commit()
    logger.info(f"{id} Post Updated Successfully !")
    return post_to_update


async def delete_post(id: int, token: str = Depends(get_auth)):
    db = next(get_db())
    deleted_post = db.query(post.Post).filter(post.Post.id == id)
    if deleted_post.first() is None:
        handle_invalid_post_id(id)
    deleted_post.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Post Deleted Succesfully !")
    


