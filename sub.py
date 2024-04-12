import time
import zmq
import json


def main():

    SERVER = "tcp://13.56.210.223:5555"

    # Establish a connection to the publisher
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(SERVER)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        try:
            # flags=NOBLOCK raises ZMQError if no messages have arrived
            raw_msg = socket.recv_string(zmq.NOBLOCK)

            """
            The message arrives in the form of:
                <string: name>;<float: latitude>;<float: longitude>;<float: heading degrees>;<float: measurement>;<string: verification id>

            I feel like I want this data to be portable, so I'm going to split it (using a semicolon as the delimiter), and create JSON objects out of each message
            """
            
            split_msg = raw_msg.split(';')

            #TODO: convert to JSON?

            # time.sleep(0.5)
            # print(split_msg)
        except zmq.ZMQError as err:
            print("socket.recv_string() Error: " + str(err))



if __name__ == "__main__":
    main()