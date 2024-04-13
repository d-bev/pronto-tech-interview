"""
PROBLEM PART #1:

Write a backend storage solution to ingest the data coming from the SERVER. 

The message arrives in the form of:
    <string: name>;<float: latitude>;<float: longitude>;<float: heading degrees>;<float: measurement>;<string: verification id>
    
    Each value of float is at most 999 with only one fractional digit. 
    String values are at most length of 6. 
    It is not readily known how many unique name will be published at any point - do not make assumptions that this number is constant.

Key metrics are (per name): the mean, min, max of the measurement and the last known (Latitude, Longitude, and Heading).
    - You are free to write this in any language that you are comfortable with (Pronto mostly writes in Python and Javascript).
    - For mean, the value only needs to be accurate to one fractional digit.

    
PLAN:
    - create a connection to the SERVER via ZMQ
    - parse the incoming data
    - organize the parsed data by which unique 'name it belongs to
    - calculate the required statistics for each unique 'name'
    - prepare (and deliver) the calculated statistics for the front-end
"""
import time
import zmq
import json

DEBUG = False

def main():

    SERVER = "tcp://13.56.210.223:5555"

    # Establish a connection to the publisher
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(SERVER)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    num_errors = 0

    while True:
        try:
            # flags=NOBLOCK raises ZMQError if no messages have arrived
            raw_msg = socket.recv_string(zmq.NOBLOCK)

            """
            I can split each string into its parameters
            I can group by unique name (or maybe even by verification ID), 

            But how am I actually going to create the groups of data?
            """
            
            #TODO: convert to JSON or XML?

            #split_msg = raw_msg.split(';')

            # time.sleep(0.5)
            # print(split_msg)
            
            print(raw_msg)

        except zmq.ZMQError as err:
            print("socket.recv_string() Error: " + str(err))

            # If connection is poor, sleep so we aren't spamming the terminal with errors
            time.sleep(0.1)



if __name__ == "__main__":
    main()