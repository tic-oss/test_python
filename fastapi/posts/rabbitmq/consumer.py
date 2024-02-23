import threading
from dotenv import load_dotenv
import pika
import json
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PS = os.getenv("RABBIT_PS")
PIKA_HOST = os.getenv("PIKA_HOST")
PIKA_PORT = os.getenv("PIKA_PORT")

class RabbitMQConsumer:
    def __init__(self, queue_name, username=RABBIT_USER, password=RABBIT_PS):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials, heartbeat=15))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name
        print(' [*] Waiting for messages...... To exit press CTRL+C')
        logger.info(' [*] Waiting for messages To exit press CTRL+C')
        
     

    def callback(self, ch, method, body):
        try:
            new_post = json.loads(body.decode())
            print("Received item:", new_post)
            logger.info(new_post)  
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
            logger.info("Error decoding JSON:", str(e))
        except Exception as e:
            print("Error processing message:", str(e))
            logger.info("Error processing message:", str(e))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    
    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        logger.info('Start listening to messages... ')
        self.channel.start_consuming()


# import threading
# from dotenv import load_dotenv
# import pika
# import json
# import os
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()
# RABBIT_USER = os.getenv("RABBIT_USER")
# RABBIT_PS = os.getenv("RABBIT_PS")
# PIKA_HOST = os.getenv("PIKA_HOST")
# PIKA_PORT = os.getenv("PIKA_PORT")

# class RabbitMQConsumer:
#     def __init__(self, queue_name, username=RABBIT_USER, password=RABBIT_PS):
#         self.queue_name = queue_name
#         credentials = pika.PlainCredentials(username, password)
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(PIKA_HOST, port=int(PIKA_PORT), credentials=credentials, heartbeat=5))
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue=queue_name)
#         logger.info(f'[*] Waiting for messages in queue {queue_name}. To exit press CTRL+C')

#     def callback(self, ch, method, properties, body):
#         try:
#             new_post = json.loads(body.decode())
#             logger.info(f"Received item: {new_post}")
#         except json.JSONDecodeError as e:
#             logger.error(f"Error decoding JSON: {e}")
#         except Exception as e:
#             logger.error(f"Error processing message: {e}")

#         ch.basic_ack(delivery_tag=method.delivery_tag)

  
#     def start_consuming(self):
#         self.channel.basic_qos(prefetch_count=1)
#         self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
#         logging.info('Start listening to messages... ')
#         self.channel.start_consuming()


# if __name__ == "__main__":
#     # Example usage
#     consumer = RabbitMQConsumer(queue_name="testqueue")
#     consumer_thread = threading.Thread(target=consumer.start_consuming)
#     consumer_thread.start()
# #    start_consuming()
