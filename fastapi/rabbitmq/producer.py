import pika
import json

class RabbitMQProducer:
    def __init__(self, queue_name):
        self.rabbitmq_params = pika.ConnectionParameters('localhost', port=5672)
        self.connection = pika.BlockingConnection(self.rabbitmq_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, routing_key, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=json.dumps(message)
        )

    