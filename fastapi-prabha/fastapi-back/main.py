from fastapi import FastAPI
import httpx
import os
import models
from database import engine
import posts
from py_eureka_client import eureka_client
from fastapi.responses import JSONResponse
import py_eureka_client.eureka_client as eureka_client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()




async def startup_event():
    await eureka_client.init_async(eureka_server=os.getenv("eureka_server"),
                                   app_name=os.getenv("app_name"),
                                   instance_port=int(os.getenv("your_rest_server_port")))

async def shutdown_event():
    await eureka_client.init_async()

# Register the startup and shutdown event handlers
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)




# Endpoint to call Microservice 2 and get its URL
@app.get("/")
async def read_root():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(os.getenv("get_url_microservice2"))
            response.raise_for_status()
            data = response.json()
            microservice2_url = data["microservice2_url"]
        return {"message": f"Hello from Microservice 1! Microservice 2 URL: {microservice2_url}"}
    except httpx.RequestError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
# eureka_client.init(eureka_server="http://localhost:8761/eureka/apps", app_name="fastapi-post")


# The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
# async def init_eureka_client():
#     await asyncio.sleep(0.1)  # Introduce a small delay to allow FastAPI to set up its event loop
#     await eureka_client.init_async()

# # Register Eureka client before the server starts
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(init_eureka_client())

# # Unregister Eureka client before the server stops
# @app.on_event("shutdown")
# async def shutdown_event():
#     await eureka_client.fini_async()






# #this is for Keycloak integration 
# # we just provide token URL and install pip install python-multipart
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8080/realms/djangorealm/protocol/openid-connect/token")

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# @app.get("/")
# # for every api we need to add "async" and (token: str = Depends(oauth2_scheme)) for every API to Authenticate
# async def read_root(token: str = Depends(oauth2_scheme)):
#     return {"token": "hi"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None, token: str = Depends(oauth2_scheme)):
#     return {"item_id": item_id, "q": q}

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, token: str = Depends(oauth2_scheme)):
#     return {"item_name": item.name, "item_id": item_id}


# # Register with JHipster Registry
# jhipster_registry_url = "http://localhost:8761/eureka/apps"
# microservice_name = "fastapi-post"

# requests.post(
#     f"{jhipster_registry_url}/apps/{microservice_name}",
#     json={
#         "instance": {
#             "hostName": "fastapi-post",
#             "app": "fastapi-post",
#             "ipAddr": "localhost",
#             "status": "UP",
#             "port": {"$": 8000, "@enabled": "true"},
#             "vipAddress": "fastapi-post",
#             "secureVipAddress": "fastapi-post",
#             "dataCenterInfo": {"@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo", "name": "MyOwn"},
#         }
#     },
# )

models.Base.metadata.create_all(bind=engine)
app.include_router(posts.router)