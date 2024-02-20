from posts.database import engine
from fastapi import FastAPI
import posts.models
import posts.posts
import posts.schema
import eureka

app = FastAPI()


# Register the startup and shutdown event handlers
# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)
app.include_router(eureka.router)



# posts
posts.models.Base.metadata.create_all(bind=engine)
app.include_router(posts.posts.router)