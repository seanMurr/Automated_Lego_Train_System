#!/usr/bin/env python3

# takes command line arguments to test the serialComs.py module
# usage $python3 testHubComs.py [port],0,[hubID],[speed]
# ie to set speed of hubID 2 attached to ttyUSB1 to 30%
# $python3 testHubComs.py 1,0,2,30

import serial, time, sys
import hubComs

if __name__ == '__main__':

    # ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    # ser.flush()
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # if len(sys.argv)-1 == 2:
    #     print((sys.argv[1]+" "+sys.argv[2]+"\n").encode())
    #     ser.write((sys.argv[1]+" "+sys.argv[2]+"\n").encode())

    print('Number of arguments:', len(sys.argv), 'arguments.')
    msg = ""
    port = "/dev/ttyUSB"+sys.argv[1]
    for i in range(len(sys.argv)-2):
        msg = msg + sys.argv[i+2]
        print(port)
    print(msg)
    # hubComs.sendToHub('/dev/ttyUSB0',msg)
    hubComs.sendToHub(port,msg)
