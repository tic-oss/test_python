from py_eureka_client import eureka_client
from dotenv import load_dotenv
from fastapi import APIRouter
import os
import requests
import xml.etree.ElementTree as ET

load_dotenv()

EUREKA_SERVER = os.getenv("EUREKA_SERVER")
APP_NAME = os.getenv("APP_NAME")
POST_PORT = os.getenv("POST_PORT")
OTHER_SERVICE_NAME = os.getenv("OTHER_SERVICE_NAME")
EUREKA_SERVER_INSTANCES = os.getenv("EUREKA_SERVER_INSTANCES")

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


async def startup_event():
    await eureka_client.init_async(eureka_server=EUREKA_SERVER,
                                   app_name=APP_NAME,
                                   instance_port=int(POST_PORT))
    
async def shutdown_event():
    await eureka_client.fini_async()

@router.on_event("startup")
async def startup():
    await startup_event()


@router.on_event("shutdown")
async def shutdown():
    await shutdown_event()



# Endpoint to provide Slack URL
def get_microservice_url(app_name: str) -> str:
    response = requests.get(EUREKA_SERVER_INSTANCES)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for application in root.findall("./application"):
            name = application.find("name").text
            if name == app_name:
                instance = application.find("./instance")
                home_page_url = instance.find("homePageUrl").text
                return home_page_url
        return None
    else:
        raise Exception(f"Failed to fetch applications from Eureka server: {response.status_code}")

# Example usage:
    
@router.get("/get_other")
def get_other():
    microservice_url = get_microservice_url(OTHER_SERVICE_NAME)
    return {"url":microservice_url}
