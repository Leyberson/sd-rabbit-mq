import os
from actuators import actuators_pb2_grpc
from actuators import actuators_pb2
import grpc
import time


def run():
    pid = os.getpid()

    with grpc.insecure_channel('localhost:50001') as channel:
        stub = actuators_pb2_grpc.ActuatorStub(channel)
        start = time.time()
        response = stub.turn_on(actuators_pb2.Action())

        print(response)


if __name__ == '__main__':
    run()
