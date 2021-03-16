import pika
import time

HOST = 'localhost'
QUEUE_NAME = 'sensor'
MESSAGE = "Alguma Messagem"

connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST))
channel = connection.channel()


for i in range(1, 1000):
    channel.basic_publish(exchange="", routing_key = QUEUE_NAME, body=MESSAGE)
    print(f" [x] Sent {MESSAGE}")
    time.sleep(1)

connection.close()