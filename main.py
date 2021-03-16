from reciever import Receiver
import threading as th
from ilumination.lamp import Lamp

HOST = 'localhost'
count = 0


def main():
    receiver_sensor = Receiver(queue_name = 'sensor')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")