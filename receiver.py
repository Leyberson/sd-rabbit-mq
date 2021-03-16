import pika


class Receiver:
    def __init__(self, queue_name, host='localhost'):
        self.queue_name = queue_name
        self.host = host

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        self.channel = self.connection.channel()

        self.start_consuming()

    def start_consuming(self):
        self.channel.queue_declare(queue = self.queue_name)

        def callback(ch, method, properties, body):
            # todo this method will send a message to a handler
            print(f" [*] Received %r" % body.decode())

        self.channel.basic_consume(queue = self.queue_name, on_message_callback = callback, auto_ack = True)
        print(f" [*] Waiting for message. To exit press CTRL+C")
        self.channel.start_consuming()
