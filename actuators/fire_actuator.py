import grpc
from concurrent import futures


class Light:
    def __init__(self):
        self.turned_on = False
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
        self.server.add_insecure_port('[::]:50051')
        self.server.start()
        self.server.wait_for_termination()

    def turn_on(self):
        self.turned_on = True

    def turn_off(self):
        self.turned_on = False

    def __str__(self):
        return f"The fire controller is turned {'on' if self.turned_on else 'off'}"
