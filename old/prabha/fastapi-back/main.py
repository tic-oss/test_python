from fastapi import FastAPI
import os
import models
from database import engine
import posts
from py_eureka_client import eureka_client
from dotenv import load_dotenv
import asyncio
import requests
import xml.etree.ElementTree as ET

asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()

app = FastAPI()


async def startup_event():
    await eureka_client.init_async(
        eureka_server=os.getenv("eureka_server"),
        app_name=os.getenv("app_name"),
        instance_port=int(os.getenv("microservice1_port"))
    )


async def shutdown_event():
    await eureka_client.fini_async()


# Register the startup and shutdown event handlers
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


def get_microservice_url(app_name: str) -> str:
    # Make a GET request to the Eureka server to fetch the applications information
    response = requests.get(os.getenv("eureka_server_instances"))
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)
        # Iterate through each application
        for application in root.findall("./application"):
            name = application.find("name").text
            if name == app_name:
                # If the application name matches, extract and return the URL of the first instance
                instance = application.find("./instance")
                home_page_url = instance.find("homePageUrl").text
                return home_page_url
        # If no matching application is found, return None
        return None
    else:
        # If the request fails, raise an exception
        raise Exception(f"Failed to fetch applications from Eureka server: {response.status_code}")

# Example usage:
    
@app.get("/get_other")
def get_other():
    microservice_url = get_microservice_url(os.getenv("other_service_name"))
    return {"url":microservice_url}


@app.get("/hi")
async def get_microservice2_url():
    return {"message": "hii....hi am prabha from microservice1"}   

models.Base.metadata.create_all(bind=engine)
app.include_router(posts.router)




