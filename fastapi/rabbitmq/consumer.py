import pika
import json

class RabbitMQConsumer:
    def __init__(self, queue_name):
        self.rabbitmq_params = pika.ConnectionParameters('localhost', port=5672)
        self.connection = pika.BlockingConnection(self.rabbitmq_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

    def callback(self, ch, method, properties, body):
        try:
            new_post = json.loads(body.decode())
            print("Received item:", new_post)
            # Validate the received data against the schema here if needed
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        print('Consumer is waiting for messages. To exit, press CTRL+C')
        self.channel.start_consuming()

   



        
        