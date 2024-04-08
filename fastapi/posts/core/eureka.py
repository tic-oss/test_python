import json
import logging
from core.auth import *
from fastapi import APIRouter, HTTPException
import os
from fastapi import Depends
from py_eureka_client.eureka_client import EurekaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

EUREKA_SERVER = os.getenv("EUREKA_SERVER")
APP_NAME = os.getenv("APP_NAME")
POST_PORT = os.getenv("POST_PORT")
OTHER_SERVICE_NAME = os.getenv("OTHER_SERVICE_NAME")
EUREKA_SERVER_INSTANCES = os.getenv("EUREKA_SERVER_INSTANCES")
PUBLIC_IP = os.getenv("PUBLIC_IP", "0.0.0.0") 
OTHER_SERVICE_URL=os.getenv("OTHER_SERVICE_URL")


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


client = None

async def startup_event():
    global client
    try:
        client = EurekaClient(
            eureka_server=EUREKA_SERVER,
            app_name=APP_NAME,
            instance_port=int(POST_PORT),
            instance_ip=PUBLIC_IP
        )
        await client.start()
    except Exception as e:
        # Handle initialization errors
        print(f"Error during startup: {e}")

async def shutdown_event():
    if client:
        try:
            await client.stop()
        except Exception as e:
            # Handle shutdown errors
            print(f"Error during shutdown: {e}")



@router.get("/get_response_from_slack")
async def get_response_from_slack(token: str = Depends(oauth2_scheme)):
    try:
        # Check if the client has been initialized
        if client is None:
            raise HTTPException(status_code=500, detail="Client not initialized")
        
        headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'} 
        res = await client.do_service(OTHER_SERVICE_NAME, OTHER_SERVICE_URL, headers=headers)
        json_res = json.loads(res)
        return {"Response of other microservice": json_res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







