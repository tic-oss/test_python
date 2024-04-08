from dotenv import load_dotenv
load_dotenv()
from core.database import engine
from fastapi import FastAPI
import models.post
import routers.post
import core.eureka as eureka


app = FastAPI()


# Register the startup and shutdown event handlers
app.add_event_handler("startup", eureka.startup_event)
app.add_event_handler("shutdown", eureka.shutdown_event)
app.include_router(eureka.router)

# posts
models.post.Base.metadata.create_all(bind=engine)
app.include_router(routers.post.router)

