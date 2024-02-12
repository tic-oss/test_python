
from fastapi import Depends, FastAPI
import posts.models
from posts.database import engine
import posts.posts
import posts.schema
from py_eureka_client import eureka_client
import py_eureka_client.eureka_client as eureka_client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


async def startup_event():
    await eureka_client.init_async(eureka_server=os.getenv("eureka_server"),
                                   app_name=os.getenv("app_name"),
                                   instance_port=int(os.getenv("microservice2_port")))


async def shutdown_event():
    await eureka_client.fini_async()

# Register the startup and shutdown event handlers
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


your_rest_server_port=int(os.getenv("microservice2_port"))
# Endpoint to provide Microservice 2 URL
@app.get("/get_microservice2_url")
async def get_microservice2_url():
    return {"microservice2_url": f"http://localhost:{your_rest_server_port}"}   


# posts

posts.models.Base.metadata.create_all(bind=engine)
app.include_router(posts.posts.router)

# slack
# app.include_router(slack.slack.router)