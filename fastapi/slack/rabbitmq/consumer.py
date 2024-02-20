from dotenv import load_dotenv
import pika
import json
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PS = os.getenv("RABBIT_PS")
PIKA_HOST = os.getenv("PIKA_HOST")
PIKA_PORT = os.getenv("PIKA_PORT")

class RabbitMQConsumer:
    def __init__(self, queue_name, username=RABBIT_USER, password=RABBIT_PS):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name
        print(' [*] Waiting for messages. To exit press CTRL+C')
        logging.info(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(self, ch, method, body):
        try:
            new_post = json.loads(body.decode())
            print("Received item:", new_post)
            logging.info(new_post)   
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
            logging.info("Error decoding JSON:", str(e))
        except Exception as e:
            print("Error processing message:", str(e))
            logging.info("Error processing message:", str(e))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    
    def start_consuming(self, queue_name):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        logging.info('Start listening to messages... ')
        self.channel.start_consuming()