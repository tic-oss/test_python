from backend.database import engine
from fastapi import FastAPI
import models.models
import routers.posts
import schemas.schema
import services.eureka as eureka
import uvicorn

app = FastAPI()


# Register the startup and shutdown event handlers
app.add_event_handler("startup", eureka.startup_event)
app.add_event_handler("shutdown", eureka.shutdown_event)
app.include_router(eureka.router)



# posts
models.models.Base.metadata.create_all(bind=engine)
app.include_router(routers.posts.router)

