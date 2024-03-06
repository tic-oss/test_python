from dotenv import load_dotenv
import pika
import os
import asyncio
import aio_pika
import logging
# import slack.eureka as eureka 
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PS = os.getenv("RABBIT_PS")
PIKA_HOST = os.getenv("PIKA_HOST")
PIKA_PORT = os.getenv("PIKA_PORT")

class RabbitMQConsumer:
    def __init__(self, exchange_name, queue_name, binding_keys, username=RABBIT_USER, password=RABBIT_PS):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.binding_keys = binding_keys
        self.connection = None
        self.channel = None
        self.username = username
        self.password = password

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(
                host=PIKA_HOST,
                port=int(PIKA_PORT),
                login=self.username,
                password=self.password
            )
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)

            await self.channel.declare_exchange(
                self.exchange_name,
                type=aio_pika.ExchangeType.DIRECT
            )

            queue = await self.channel.declare_queue(
                self.queue_name,
                durable=True
            )

            for binding_key in self.binding_keys:
                await queue.bind(
                    exchange=self.exchange_name,
                    routing_key=binding_key
                )

            logger.info(' [*] Waiting for messages. To exit press CTRL+C')
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")

    async def callback(self, message):
        async with message.process():
            body = message.body.decode()
            logger.info(f"Received message: {body}")

    async def start_consuming(self):
        try:
            await self.connect()

            queue = await self.channel.get_queue(self.queue_name)
            await queue.consume(self.callback)
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")


# class RabbitMQConsumer:
#     def __init__(self, exchange_name, queue_name, binding_keys, username=RABBIT_USER, password=RABBIT_PS):
#         logger.info("Initializing RabbitMQConsumer...")
#         credentials = pika.PlainCredentials(username, password)
#         try:
#             self.connection = pika.BlockingConnection(
#                 pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials))
#             logger.info("Connection established")
#         except Exception as e:
#             logger.error(f"Error connecting to RabbitMQ: {e}")
#             return
        
#         self.channel = self.connection.channel()
#         self.exchange_name = exchange_name
#         self.queue_name = queue_name
#         self.binding_keys = binding_keys

#         # Declare the exchange
#         self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

#         # Declare the queue
#         self.channel.queue_declare(queue=queue_name, durable=True)

#         # Bind the queue to the exchange with the provided binding keys
#         for binding_key in binding_keys:
#             self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

#         logger.info(' [*] Waiting for messages. To exit press CTRL+C')
#         # print(" [*] Waiting for messages. To exit press CTRL+C")
#     def callback(self, ch, method, properties, body):
#         try:
#             message = body.decode()
#             logger.info(f"Received message: {message}")
#         except Exception as e:
#             logger.error(f"Error processing message: {str(e)}")

#         ch.basic_ack(delivery_tag=method.delivery_tag)

#     def start_consuming(self):
#         self.channel.basic_qos(prefetch_count=1)
#         self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
#         self.channel.start_consuming()







