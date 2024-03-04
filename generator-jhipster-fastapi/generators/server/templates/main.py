<%_ if (postgresql){  _%>
from backend.database import engine
from models import models
from routers import posts
from schemas import schema
<%_ } _%>

<%_ if (mongodb){  _%>
from routers import slack
<%_ } _%>

from fastapi import FastAPI
from services import eureka
import uvicorn

app = FastAPI()

app.include_router(eureka.router)

<%_ if (postgresql){  _%>
# posts
posts.models.Base.metadata.create_all(bind=engine)
app.include_router(posts.posts.router)
<%_ } _%>

<%_ if (mongodb){  _%>
app.include_router(slack.slack.router)
<%_ } _%>