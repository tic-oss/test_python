from fastapi import APIRouter, Depends, status
from typing import List
from services.slack_service import *
from models.slack import Message
from .router_utils import *
from core.keycloak import oauth2_scheme
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
    return get_channels()


@router.get("/messages/{channel}", response_model=List[Message])
async def get_messages(channel: str, token: str = Depends(oauth2_scheme)):
    logger.info(f"request / endpoint!")
    """Get all messages for the specified channel."""
    return get_messages(channel)


@router.post("/post_message", status_code=status.HTTP_201_CREATED)
async def post_message(message: Message, token: str = Depends(oauth2_scheme)):
    """Post a new message to the specified channel."""
    ack = insert_message(message)
    logger.info(f"request / endpoint!")
    return {"insertion": ack}


@router.put("/update_message/{message_id}", status_code=status.HTTP_200_OK)
async def update_message(message_id: str, updated_message: Message, token: str = Depends(oauth2_scheme)):
    """Update an existing message with the specified ID."""
    if not update_message(message_id, updated_message):
        handle_message_not_found()
    logger.info(f"request / endpoint!")
    return {"message": "Update successful"}


@router.delete("/delete_message/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: str, token: str = Depends(oauth2_scheme)):
    """Delete a message with the specified ID."""
    if not delete_message(message_id):
        handle_message_not_found()
    logger.info(f"request / endpoint!")
    return {"message": "Deletion successful"}




