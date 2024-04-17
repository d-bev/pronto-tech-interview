"""
PROBLEM PART #1:

Write a backend storage solution to ingest the data coming from the SERVER. 

The message arrives in the form of:
    <string: name>;<float: latitude>;<float: longitude>;<float: heading degrees>;<float: measurement>;<string: verification id>
    
    Each value of float is at most 999 with only one fractional digit. 
    String values are at most length of 6. 
    !!! Do not assume that the number of unique names is constant

Key metrics are (per name): the mean, min, max of the measurement and the last known (Latitude, Longitude, and Heading).
    - the mean only needs to be accurate to one fractional digit.
    
PLAN:
    - create a connection to the SERVER via ZMQ
    - organize the data by which unique 'name' it belongs to
    - calculate the required statistics for each unique 'name'
    - prepare the calculated statistics for the front-end
    - either deliver the processed data to the front-end, or make it requestable by the front-end
"""
import time
import zmq
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

DEBUG = True
MAX_ITERATIONS = 5

data = {}


#   Set up Flask to bypass CORS at the front end:
app = Flask(__name__)
cors = CORS(app)

#Create the receiver API POST endpoint:
@app.route("/receiver", methods=["GET"])
def get_data():
   data = {
        "name": "Steve",
        "dob": 1942,
        "mother": "yours!",
   }

   data = jsonify(data)
   return data

def main():

    SERVER = "tcp://13.56.210.223:5555"

    # Establish a connection to the publisher
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(SERVER)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    """
    DESIRED RESULT:
        (per name): mean, min, max of 'measurement', most recent (Latitude, Longitude, and Heading).
            the mean only needs to be accurate to one fractional digit.

    ASSUMPTIONS:

        If I'm to calculate the mean:
            I need the sum of all previous entries (and then add the most recent entry to it)
            The amount of previous entries (and then add 1 for the entry coming in)
    
        I'll probably need to group by name, as it's the only paramter that could operate as a Primary Key

        Probably need to use a dict to store all of the data
            Can use 'name' as the key
            they're hash-tables "under the hood", so lookups are O(1)

    THOUGHTS:
        
        So I guess I'll build a dict, and:
            Add a parameter to the key's values to track how many times it's been accessed
            Add a parameter to the key's values to track the previous sum (of the measurement)

            If the value exists in the dict already:
                Do a basic "less/greater than" comparison to determine the min and max (of the measurement)
                Replace the Lat, Lon, and Heading params
            Else:
                Create the value to be assigned to the key
                    [sum, n, min, max, mean, (Lat, Lon, Heading)]
                Create the dict entry
                    name -> sum, n, min, max, mean, (Lat, Lon, Heading)

        The data I'm working with is coming in very quickly!
            Should I make this program just process one message at a time?
                Sounds simpler (utilize useState hook to update the state once per message)
                Might actually be more expensive performance-wise (because we're making a lot of calls + Python overhead)
                    But also might be better for the front-end, as it doesn't have to un-nest the JSON it's being passed
            Or should I leave the connection open and process messages in batches?
                Leaving the connection open means we aren't missing messages
                Having delays between pushing data to the frontend would probably make the frontend feel more responsive

            TL;DR -> Should I sacrifice performance on the backend or the front end?
                I want to say it's better to make the backend do more work, just so the front-end feels smoother, but I really don't know

        How to transfer data between files?
            Writing to a static file is entirely out of the question
            It should probably be formatted as JSON or XML, so I'm going to choose JSON (personal preference)

            I'm going to try to use Flask, and structure this project such that:
                This file will be continuously running and collecting data
                There will be a button on the front-end that triggers a GET request
                    The GET request (received by this program) will prompt the app to return the current contents of 'data'
                I can take the data returned from the request and hopefully figure out how to use REACT hooks to update the frontend
    """


    num_entries = 0

    while True:
        try:
            raw_msg = socket.recv_string() 
            # raw_msg = socket.recv_string(zmq.NOBLOCK) # flags=NOBLOCK raises ZMQError if no messages have arrived
            
            # Processing the message
            # NOTE: message arrives as:
            #           <string: name>;<float: latitude>;<float: longitude>;<float: heading degrees>;<float: measurement>;<string: verification id>

            split_msg = raw_msg.split(';')

            name = str(split_msg[0])
            measurement = float(split_msg[4])
            
            # NOTE: I'm specifically setting the values of 'min' and 'max' to be overwritten
            data[name] = dict(lat=float(split_msg[1]), lon=float(split_msg[2]), heading=float(split_msg[3]), sum=0, n=0, min=1000, max=-1000, mean=0, verif=str(split_msg[5]))
            
            # Create/Update the statistics
            
            data[name]['sum'] += measurement
            data[name]['n'] += 1

            data[name]['mean'] = round(data[name]['sum'] / data[name]['n'], 1)

            if data[name]['min'] < measurement:
                data[name]['min'] = measurement

            if data[name]['max'] > measurement:
                data[name]['max'] = measurement

            # # TODO: decide how frequently I want
            # if num_entries == MAX_ITERATIONS:
            #     print(data)
            #     break
            # else:
            #     num_entries += 1

        except zmq.ZMQError as err:
            print("socket.recv_string() raised: " + str(err))

            # If connection is poor, sleep so we aren't spamming the terminal with errors
            time.sleep(0.02)


if __name__ == "__main__": 
   app.run(debug=True)
   time.sleep(0.1)
   main()
