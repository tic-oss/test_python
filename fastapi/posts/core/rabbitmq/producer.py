import pika
import json
import os
import logging

logger = logging.getLogger(__name__)

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PS = os.getenv("RABBIT_PS")
PIKA_HOST = os.getenv("PIKA_HOST")
PIKA_PORT = os.getenv("PIKA_PORT")
EXCHANGE_NAME = "direct_logs"


class RabbitMQProducer:
    def __init__(self, exchange_name=EXCHANGE_NAME, username=RABBIT_USER, password=RABBIT_PS):
        credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None
        self.exchange_name = exchange_name
        self.connect(credentials)

    def connect(self, credentials):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials, heartbeat=550))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')
            logger.info('Connection established: {} to exchange: {}'.format(self.connection, self.exchange_name))
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Error establishing connection: {e}")
            raise e

    def publish_message(self, routing_key, message):
        try:
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=json.dumps(message)
            )
            print(f" [x] Sent {message}")
            logger.info(f" [x] Sent {message} ")
        except (pika.exceptions.ChannelClosed, pika.exceptions.StreamLostError,
                pika.exceptions.ChannelWrongStateError) as error:
            logger.error("Channel closed. Attempting to reconnect...")
            self.reconnect()

    def reconnect(self):
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PS)
        self.connect(credentials)







# import pika
# import json
# import os
# import logging
# logger = logging.getLogger(__name__)

# RABBIT_USER = os.getenv("RABBIT_USER") 
# RABBIT_PS = os.getenv("RABBIT_PS")
# PIKA_HOST = os.getenv("PIKA_HOST")
# PIKA_PORT = os.getenv("PIKA_PORT")


# class RabbitMQProducer:
#     def __init__(self, exchange_name, username=RABBIT_USER, password=RABBIT_PS):
#         credentials = pika.PlainCredentials(username, password)
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials, heartbeat=550))
#         logger.info('Connection established: {} to exchange: {}'.format(self.connection, exchange_name))
#         self.channel = self.connection.channel()
#         self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

#     def publish_message(self, routing_key, message):
#         try:
#             self.channel.basic_publish(
#                 exchange='direct_logs',
#                 routing_key=routing_key,
#                 body=json.dumps(message)
#             )
#             print(f" [x] Sent {message}")
#             logger.info(f" [x] Sent {message} ")
#         except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.StreamLostError,
#                 pika.exceptions.ChannelWrongStateError) as error:
#             print("Connection or channel closed. Attempting to reconnect...")
#             self.reconnect()

#     def reconnect(self, username=RABBIT_USER, password=RABBIT_PS):
#         credentials = pika.PlainCredentials(username, password)
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(PIKA_HOST, port=PIKA_PORT, credentials=credentials, heartbeat=5))
#         self.channel = self.connection.channel()




