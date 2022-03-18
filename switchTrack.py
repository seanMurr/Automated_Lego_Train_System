#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys,json, re, datetime,time,random

mqttServerAddress = "192.168.0.10" #e.g piserver.local or 192.168.1.100

def switchTrack(pointID, position):
    # Create an MQTT client and attach our routines to it.
    client = mqtt.Client("selfTester")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect(mqttServerAddress, 1883, 60)
    # straight ="135"
    # turn = "173"
    client.publish("lego/track/switch/" + str(pointID), position)
    # for switch in range(6):
    #     client.publish("lego/track/switch/0" + str(switch), straight)
    #     time.sleep(0.5)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print all messages that are subscribed to
    print(str(datetime.datetime.now()) +" "+msg.topic+" "+str(msg.payload))

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    pointID = sys.argv[1]
    position = sys.argv[2]
    # for i in range(len(sys.argv)-2):
    #     msg = msg + sys.argv[i+2]
    #     print(port)
    # print(msg)
    # hubComs.sendToHub('/dev/ttyUSB0',msg)
    switchTrack(pointID,position)
