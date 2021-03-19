import pika

import time
import random

HOST = 'localhost'
QUEUE_NAME = 'temperatura.sensor1'

connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST))
channel = connection.channel()
channel.queue_declare(queue = QUEUE_NAME)

try:
    while True:
        time.sleep(20)
        message = str(random.choice(range(10, 40)))
        channel.basic_publish(exchange = "", routing_key = QUEUE_NAME, body = message)
except KeyboardInterrupt:
    connection.close()