import grpc
from concurrent import futures


class Light:
    def __init__(self):
        self.turned_on = False
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
        self.temperature = None
        self.server.add_insecure_port('[::]:50052')
        self.server.start()
        self.server.wait_for_termination()

    def turn_on(self):
        if not self.turned_on:
            self.turned_on = True
            self.temperature = 25

    def turn_off(self):
        self.turned_on = False
        self.temperature = None

    def raise_temperature(self):
        if self.turned_on and self.temperature<29:
            self.temperature += 1

    def lower_temperature(self):
        if self.turned_on and self.temperature>15:
            self.temperature -= 1

    def __str__(self):
        return f"The air-conditioning is turned {f'on and temperature = {self.temperature}' if self.turned_on else 'off'}"
