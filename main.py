from receiver import Receiver

HOST = 'localhost'
count = 0


def main():
    receiver_sensor = Receiver(queue_name = 'sensor')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")