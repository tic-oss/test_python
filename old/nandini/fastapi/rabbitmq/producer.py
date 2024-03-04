from dotenv import load_dotenv
import pika
import json
import os

load_dotenv()

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PS = os.getenv("RABBIT_PS")
PIKA_HOST = os.getenv("PIKA_HOST")
PIKA_PORT = os.getenv("PIKA_PORT")


class RabbitMQProducer:
    def __init__(self, queue_name, username=RABBIT_USER, password=RABBIT_PS):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)


    def publish_message(self, routing_key, message):
        try:
            self.channel.basic_publish(
               exchange='',
               routing_key=routing_key,
               body=json.dumps(message)
            )
            print(f" [x] Sent {message}")
        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed) as error:
            print("Connection or channel closed. Attempting to reconnect...")
            self.reconnect()
      
    def reconnect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=self.connection.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)