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

DEBUG = True

def main():

    SERVER = "tcp://13.56.210.223:5555"

    # Establish a connection to the publisher
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(SERVER)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    if DEBUG:
        num_entries = 0

    data = {}

    while True:
        try:
            # flags=NOBLOCK raises ZMQError if no messages have arrived
            # raw_msg = socket.recv_string(zmq.NOBLOCK)

            raw_msg = socket.recv_string()

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

            PROTOTYPING:

                data = {
                    "name": {
                        "sum":  ,
                        "n":    ,
                        "min":  ,
                        "max":  ,
                        "mean": ,
                        "lat": ,
                        "lon": ,
                        "heading": ,
                        "verif": ,
                    },
                }

                - access this like:  data["name"]["sum"]
                - create new entries like: data["new_name"] = dict(param1 = x, param2 = y, ...)
            """

            # Processing the message
        
            split_msg = raw_msg.split(';')

            name = str(split_msg[0])
            measurement = float(split_msg[4])
            
            # <string: name>;<float: latitude>;<float: longitude>;<float: heading degrees>;<float: measurement>;<string: verification id>
            data[name] = dict(lat=float(split_msg[1]), lon=float(split_msg[2]), heading=float(split_msg[3]), sum=0, n=0, min=-1, max=1000, mean=0, verif=str(split_msg[5]))

            
            # Create/Update the statistics
            
            data[name]['sum'] += measurement
            data[name]['n'] += 1

            data[name]['mean'] = data[name]['sum'] / data[name]['n']

            if data[name]['min'] < measurement:
                data[name]['min'] = measurement

            if data[name]['max'] > measurement:
                data[name]['max'] = measurement
                # round(number, 1)

            # TODO: ?
            #json_msg = json.dumps(split_msg)

            if DEBUG:
                # print(split_msg)
                # print(raw_msg)

                if num_entries == 3:
                    print(measurement)
                    print(split_msg)
                    print(data[split_msg[0]])
                    break
                else:
                    num_entries += 1

        except KeyboardInterrupt:   
            # in case there are messages that were queued
            time.sleep(0.5)
            break

        except zmq.ZMQError as err:
            print("socket.recv_string() raised: " + str(err))

            # If connection is poor, sleep so we aren't spamming the terminal with errors
            time.sleep(0.1)

        


if __name__ == "__main__":
    main()