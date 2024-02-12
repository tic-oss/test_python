from posts.database import engine
from fastapi import FastAPI
import posts.models
import posts.posts
import posts.schema
import slack.slack

app = FastAPI()

# posts
posts.models.Base.metadata.create_all(bind=engine)
app.include_router(posts.posts.router)

# slack
app.include_router(slack.slack.router)




