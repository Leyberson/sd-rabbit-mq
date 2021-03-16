import pika

HOST = 'localhost'
QUEUE_NAME = 'Temperature Sensor'

connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST))
channel = connection.channel()
channel.queue_declare(queue = QUEUE_NAME)

try:
    while True:
        message = input("Welcome to temperature sensor type the temperature: ")
        channel.basic_publish(exchange = "", routing_key = QUEUE_NAME, body = message)
except KeyboardInterrupt:
    connection.close()