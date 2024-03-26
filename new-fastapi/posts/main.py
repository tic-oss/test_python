from dotenv import load_dotenv
load_dotenv()

from core.database import engine
from fastapi import FastAPI
from routers import notes
from routers import health_check
from core import eureka
from core.rabbitmq import producer
from routers import health_check


app = FastAPI()


app.include_router(eureka.router)
app.include_router(health_check.router)
app.include_router(producer.router)


# posts
notes.models.Base.metadata.create_all(bind=engine)
app.include_router(notes.router)
