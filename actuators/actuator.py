import grpc
from concurrent import futures
from . import actuators_pb2
from . import actuators_pb2_grpc
import time
import threading


class Actuator(actuators_pb2_grpc.ActuatorServicer):
    def __init__(self):
        self.turned = False

    def turn_on(self, request, context):
        self.turned = True
        return actuators_pb2.Turned(turned = self.turned)

    def turn_off(self, request, context):
        self.turned = False
        return actuators_pb2.Turned(turned = self.turned)


class LightActuator(Actuator):
    def __init__(self):
        super().__init__()


class FireActuator(Actuator):
    def __init__(self):
        super().__init__()


class AirConditioningActuator(Actuator):
    def __init__(self):
        super().__init__()


def serve(port, actuator_name):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 1))
    exec("actuators_pb2_grpc.add_ActuatorServicer_to_server(" +actuator_name + "(), server)")
    server.add_insecure_port("[::]:" + port)
    server.start()
    try:
        while True:
            print("server on: threads %i" % (threading.active_count()) )
            time.sleep(10)
    except InterruptedError:
        print('InterruptedError')
        server.stop(0)


if __name__ == "__main__":
    serve()