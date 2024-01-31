import pika
import json


# class RabbitMQProducer:
#     def __init__(self, queue_name):
#         self.rabbitmq_params = pika.ConnectionParameters('localhost', port=5672)
#         self.connection = pika.BlockingConnection(self.rabbitmq_params)
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue=queue_name)

#     def publish_message(self, routing_key, message):
#         self.channel.basic_publish(
#             exchange='',
#             routing_key=routing_key,
#             body=json.dumps(message)
#         )

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
# channel = connection.channel()
# channel.queue_declare(queue='hello')

# channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close()
    
# import pika
# import sys

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='task_queue', durable=True)

# message = ' '.join(sys.argv[1:]) or "Hello World!"
# channel.basic_publish(
#     exchange='',
#     routing_key='task_queue',
#     body=message,
#     properties=pika.BasicProperties(
#         delivery_mode=pika.DeliveryMode.Persistent
#     ))
# print(f" [x] Sent {message}")
# connection.close()

# import pika
# import sys

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='task_queue', durable=True)

# message = ' '.join(sys.argv[1:]) or "Hello World!"
# channel.basic_publish(
#     exchange='',
#     routing_key='task_queue',
#     body=message,
#     properties=pika.BasicProperties(
#         delivery_mode=pika.DeliveryMode.Persistent
#     ))
# print(f" [x] Sent {message}")
# connection.close()
















class RabbitMQProducer:
    def __init__(self, queue_name, username='guest', password='guest'):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('172.17.0.1', port=5672, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, routing_key, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=json.dumps(message)
        )
        print(f" [x] Sent {message}")
        #self.connection.close()