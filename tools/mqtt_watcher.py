#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys,json, re, datetime

mqttServerAddress = "10.1.1.50" #e.g piserver.local or 192.168.1.100

def main():
    # Create an MQTT client and attach our routines to it.
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqttServerAddress, 1883, 60)

    # Process network traffic and dispatch callbacks. This will also handle
    # reconnecting. Check the documentation at
    # https://github.com/eclipse/paho.mqtt.python
    # for information on how to use other loop*() functions
    client.loop_forever()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("#")  # subscribe to ALL MQTT topics
    client.subscribe("lego/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print all messages that are subscribed to
    print(str(datetime.datetime.now()) +" "+msg.topic+" "+str(msg.payload))




main()
