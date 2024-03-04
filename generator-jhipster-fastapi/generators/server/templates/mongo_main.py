from fastapi import FastAPI
from routers import slack
from services import eureka

app = FastAPI()


# Register the startup and shutdown event handlers
# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)
app.include_router(eureka.router)

# slack
