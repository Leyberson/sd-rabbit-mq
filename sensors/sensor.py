import pika
import random
import time
import threading


class Sensor:
    def __init__(self, queue_name, values, timer, weights=None, host='localhost'):
        self.queue_name = queue_name
        self.host = host
        self.values = values
        self.weights = weights
        self.timer = timer
        self.message = None

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = self.queue_name)

        th = threading.Thread(target = self.start)

        th.start()

    def start(self):
        try:
            while True:
                time.sleep(self.timer)
                self.message = random.choices(population = self.values, weights = self.weights, k = 0)
                self.channel.basic_publish(exchange = "", routing_key = self.queue_name, body = self.message)
        except KeyboardInterrupt:
            self.connection.close()