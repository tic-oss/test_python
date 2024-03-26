from dotenv import load_dotenv
load_dotenv()

from core.rabbitmq.consumer import RabbitMQConsumer
from fastapi import FastAPI
from routers import notes_mongo
from routers import health_check
from core import eureka
from core import database
import asyncio

app = FastAPI()


# Register the startup and shutdown event handlers
app.add_event_handler("startup", eureka.startup_event)
app.add_event_handler("shutdown", eureka.shutdown_event)

app.include_router(eureka.router)
app.include_router(health_check.router)


app.include_router(notes_mongo.router)

async def run_consumer():
    # Create RabbitMQ consumer instance
    consumer = RabbitMQConsumer('direct_logs', 'data_queue', ['pro_queue'])

    # Start RabbitMQ consumer asynchronously
    await consumer.start_consuming()

async def run_app():
    # Start FastAPI app
    import uvicorn
    uvicorn_config = uvicorn.Config(app, host="0.0.0.0", port=9000)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()

# Start the asyncio event loop
async def main():
    await asyncio.gather(run_consumer(), run_app())

if __name__ == "__main__":
    asyncio.run(main())