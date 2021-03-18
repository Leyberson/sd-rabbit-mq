import pika
import random
import time

HOST = 'localhost'
QUEUE_NAME = 'incendio.sensor1'

connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST))
channel = connection.channel()
channel.queue_declare(queue = QUEUE_NAME)

try:
    while True:
        time.sleep(1)
        message = random.choices(['fire', 'normal'], weights = [5, 95])
        channel.basic_publish(exchange = "", routing_key = QUEUE_NAME, body = message)
except KeyboardInterrupt:
    connection.close()
