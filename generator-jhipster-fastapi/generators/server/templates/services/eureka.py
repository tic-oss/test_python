from py_eureka_client import eureka_client
from dotenv import load_dotenv
from fastapi import APIRouter
import os
import requests
import xml.etree.ElementTree as ET
from services.keycloak import oauth2_scheme
from fastapi import Depends
import json
import xmltodict 
import logging


load_dotenv()

EUREKA_SERVER = os.getenv("EUREKA_SERVER")
APP_NAME = os.getenv("APP_NAME")
PORT= os.getenv("PORT")
OTHER_SERVICE_NAME = os.getenv("OTHER_SERVICE_NAME")
EUREKA_SERVER_INSTANCES = os.getenv("EUREKA_SERVER_INSTANCES")
PUBLIC_IP = os.getenv("PUBLIC_IP", "0.0.0.0") 
OTHER_SERVICE_URL=os.getenv("OTHER_SERVICE_URL")


router = APIRouter(
    prefix='/<%= baseName %>',
    tags=['<%= baseName %>']
)



async def startup_event():
    await eureka_client.init_async(eureka_server=EUREKA_SERVER,
                                   app_name=APP_NAME,
                                   instance_port=int(PORT),
                                   instance_ip=PUBLIC_IP)
    
async def shutdown_event():
    await eureka_client.fini_async()

@router.on_event("startup")
async def startup():
    await startup_event()


@router.on_event("shutdown")
async def shutdown():
    await shutdown_event()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint to provide POSTS URL
@router.get("/get_other")
def get_other():
    response = requests.get(EUREKA_SERVER_INSTANCES)
    app_name = OTHER_SERVICE_NAME
    xml_string = response.text  
    response_slack_url = xml_to_json(xml_string, app_name)
    return {"response_slack_url": response_slack_url}

def xml_to_json(xml_string, app_name, token: str = Depends(oauth2_scheme)):
    data_dict = xmltodict.parse(xml_string)
    json_string = json.dumps(data_dict)
    json_file= json.loads(json_string)

    # Extract application information
    applications = json_file.get("applications", {}).get("application", [])
   
    for application in applications:
        if application.get("name") == app_name:
            instances = application.get("instance", [])
            if not isinstance(instances, list):
                instances = [instances]
            for instance in instances:
                ip_address = instance.get("ipAddr", "")
                port = instance.get("port", {}).get("#text", "")
                base_url = f"http://{ip_address}:{port}"
                response_slack_url = f"{base_url}{OTHER_SERVICE_URL}"
                print(response_slack_url)
                response = requests.get(response_slack_url , headers={"Authorization": f"Bearer {token}"})
                return response.json()
           
    return {"error": "No instance found for the given app name"}