#!/usr/bin/env python3

# sends a message (msg) out to serial port (port)
# port is the usb port that the bluetooth communication device is connected
# To set speed of a hub send msg "1,[hubId],[speed]"
# eg Set hubID 3, on USBport 0, to speed 20
# eg hubComs.py 0 1,3,20

# to setup a hub send the following messages
#   "0" to put device into configure mode
#   "[hubId]" the id of the hub. Each module can handle 3 hubs with id 0,1,or 2
#   "[bluetooth address]" in the format "00:11:22:33:44:55"
#   "[engineName]" the name for the engine 20 char max
#   "[dirA],[dirB]" the direction of the motor connected to each port. 0 means no motor

import serial, time, sys

def sendToHub(port, msg):
    ser = serial.Serial(port, 115200, timeout=1)
    ser.flush()
    print("Hub msg: "+msg)
    ser.write((msg+"\n").encode())

if __name__ == '__main__':

    print('Number of arguments:', len(sys.argv), 'arguments.')
    msg = ""
    port = "/dev/ttyUSB"+sys.argv[1]
    for i in range(len(sys.argv)-2):
        msg = msg + sys.argv[i+2]
        print(port)
    print(msg)
    # hubComs.sendToHub('/dev/ttyUSB0',msg)
    sendToHub(port,msg)
