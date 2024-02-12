import pika
import json




# class RabbitMQConsumer:
#     def __init__(self, queue_name):
#         self.rabbitmq_params = pika.ConnectionParameters('localhost', port=5672)
#         self.connection = pika.BlockingConnection(self.rabbitmq_params)
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue=queue_name)
#         self.queue_name = queue_name
#         self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

#     def callback(self, ch, method, properties, body):
#         try:
#             new_post = json.loads(body.decode())
#             print("Received item:", new_post)
#             # Validate the received data against the schema here if needed
#         except json.JSONDecodeError as e:
#             print("Error decoding JSON:", str(e))
#         except Exception as e:
#             print("Error processing message:", str(e))

#         ch.basic_ack(delivery_tag=method.delivery_tag)

#     def start_consuming(self):
#         print('Consumer is waiting for messages. To exit, press CTRL+C')
#         self.channel.start_consuming()



# def main():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
#     channel = connection.channel()

#     channel.queue_declare(queue='hello')

#     def callback(ch, method, properties, body):
#         print(f" [x] Received {body}")

#     channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
        
# import pika
# import time
# import json

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='task_queue', durable=True)
# print(' [*] Waiting for messages. To exit press CTRL+C')


# def callback(ch, method, properties, body):
#     print(f" [x] Received {body.decode()}")
#     time.sleep(body.count(b'.'))
#     print(" [x] Done")
#     ch.basic_ack(delivery_tag=method.delivery_tag)


# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(queue='task_queue', on_message_callback=callback)

# channel.start_consuming()     




##########################################

class RabbitMQConsumer:
    def __init__(self, queue_name, username='guest', password='guest'):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('172.17.0.1', port=5672, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name
        print(' [*] Waiting for messages. To exit press CTRL+C')
     

    def callback(self, ch, method, properties, body):
        try:
            new_post = json.loads(body.decode())
            print("Received item:", new_post)
            # Validate the received data against the schema here if needed
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
        except Exception as e:
            print("Error processing message:", str(e))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self, queue_name):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        self.channel.start_consuming()