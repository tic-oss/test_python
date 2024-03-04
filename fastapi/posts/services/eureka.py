import json
import xmltodict
import logging
from urllib import response
from py_eureka_client import eureka_client
from dotenv import load_dotenv
from fastapi import APIRouter
import os
import requests
import xml.etree.ElementTree as ET
from posts.keycloak import oauth2_scheme
from fastapi import Depends
# from fastapi.security import OAuth2PasswordBearer

load_dotenv()

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


async def startup_event():
    await eureka_client.init_async(eureka_server=EUREKA_SERVER,
                                   app_name=APP_NAME,
                                   instance_port=int(POST_PORT),
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


@router.get("/get_other")
def get_other():
    response = requests.get(EUREKA_SERVER_INSTANCES)
    app_name = OTHER_SERVICE_NAME
    xml_string = response.text  # Extract XML content from the response
    # print("XML Response:", xml_string)  # Debug print
    response_slack_url = xml_to_json(xml_string, app_name)
    # print("Parsed JSON Data:", json_data)  # Debug print
    return {"response_slack_url": response_slack_url}

def xml_to_json(xml_string, app_name, token: str = Depends(oauth2_scheme)):
    # Parse XML string into a Python dictionary
    data_dict = xmltodict.parse(xml_string)
    # print(data_dict)
    json_string = json.dumps(data_dict)
    # print(json_string)
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
                # print(response.json())
                return response.json()
           
    return {"error": "No instance found for the given app name"}