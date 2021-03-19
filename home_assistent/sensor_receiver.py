import pika

import grpc
import os
import sys
import time
import threading

new_path = os.path.abspath("")
sys.path.append(new_path)

from actuators import actuators_pb2_grpc, actuators_pb2


class Receiver:
    def __init__(self, queue_name, host='localhost'):
        self.queue_name = queue_name
        self.host = host
        self.last_message = None
        self.grpc_response = None

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        self.channel = self.connection.channel()

        th = threading.Thread(target = self.start)
        th.start()

    def start(self):
        self.channel.queue_declare(queue = self.queue_name)
        self.channel.basic_consume(queue = self.queue_name, on_message_callback = self.callback, auto_ack = True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        self.last_message = body.decode


class LightReceiver(Receiver):
    def __init__(self, queue_name, host='localhost'):
        super().__init__(queue_name, host)

    def callback(self, ch, method, properties, body):
        self.last_message = body.decode()
        if self.last_message == 'too shiny':
            with grpc.insecure_channel('localhost:50001') as channel:
                stub = actuators_pb2_grpc.ActuatorStub(channel)
                try:
                    response = stub.turn_off(actuators_pb2.Turned())
                    self.grpc_response = response
                except Exception as e:
                    print("não foi possível se comunicar com o servidor grpc")
                    print(e)

        elif self.last_message == 'too dark':
            with grpc.insecure_channel('localhost:50001') as channel:
                stub = actuators_pb2_grpc.ActuatorStub(channel)
                try:
                    response = stub.turn_on(actuators_pb2.Turned())
                    self.grpc_response = response
                    print(response)
                except:
                    print("não foi possível se comunicar com o servidor grpc")


class FireReceiver(Receiver):
    def __init__(self, queue_name, host='localhost'):
        super().__init__(queue_name, host)

    def callback(self, ch, method, properties, body):
        self.last_message = body.decode()
        if self.last_message == 'fogo':
            print("Acionar atuador")
        else:
            print("Desacionar atuador")


class AirConditioningReceiver(Receiver):
    def __init__(self, queue_name, host='localhost'):
        super().__init__(queue_name, host)

    def callback(self, ch, method, properties, body):
        self.last_message = body.decode()
        if int(self.last_message) < 20:
            print("Aumentar temperatura")
        elif int(self.last_message) >= 30:
            print("Ligar ar-condicionado ou baixar a temperatura")
