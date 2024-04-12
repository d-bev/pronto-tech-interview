import time
import zmq
import json

SERVER = "tcp://13.56.210.223:5555"

def main():

    # Establish a connection to the publisher
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(SERVER)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        msg = socket.recv_string()
        print(msg)

if __name__ == "__main__":
    main()