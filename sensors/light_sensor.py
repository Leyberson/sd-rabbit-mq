import pika

import time
import random

HOST = 'localhost'
QUEUE_NAME = 'iluminacao.sensor1'

connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST))
channel = connection.channel()
channel.queue_declare(queue = QUEUE_NAME)

try:
    while True:
        time.sleep(10)
        message = random.choice(['too dark', 'nice', 'too shiny'])
        channel.basic_publish(exchange = "", routing_key = QUEUE_NAME, body = message)
except KeyboardInterrupt:
    connection.close()
