class Lamp:
    def __init__(self, location='room'):
        self.turned_on = False
        self.location = location

    def turn_on(self):
        self.turned_on = True

    def turn_off(self):
        self.turned_on = False

    def __str__(self):
        return f"The {self.location}'s light is {'on' if self.turned_on else 'off'}"
