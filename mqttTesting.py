#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys, time

printCounts = True
numCars = 8
idCars=[0]*numCars
countCars=[[0]*3 for i in range(numCars)]
lastTrig = None
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lego/#")
    # client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global countSeg, lastTrig
    print(str(int(time.time()))+" " + msg.topic+" "+str(msg.payload))
    found = False
    sensorId = ""
    if "00" in msg.topic:
        sensorId = 0
    if "01" in msg.topic:
        sensorId = 1
    if "02" in msg.topic:
        sensorId = 2

    for car in range(numCars):
        if idCars[car] == str(msg.payload):
            found = True
            countCars[car][sensorId] += 1

    if not found:
        car = 0
        while idCars[car] != 0:
            car +=1
        idCars[car] = str(msg.payload)
        countCars[car][sensorId] += 1

    # if "lego/segment00/sensor/start" in msg.topic:
    #     if lastTrig != 0:
    #         countSeg[0] += 1
    #         lastTrig = 0
    # if "lego/segment01/sensor/start" in msg.topic:
    #     if lastTrig != 1:
    #         if lastTrig != 1:
    #             countSeg[1] += 1
    #             lastTrig = 1
    # if "lego/segment02/sensor/start" in msg.topic:
    #     if lastTrig != 2:
    #         countSeg[2] += 1
    #         lastTrig = 2
    # if "lego/segment03/sensor/start" in msg.topic:
    #     if lastTrig != 3:
    #         countSeg[3] += 1
    #         lastTrig = 3
    # if "lego/segment04/sensor/start" in msg.topic:
    #     if lastTrig != 4:
    #         countSeg[4] += 1
    #         lastTrig = 4
    # if "lego/segment05/sensor/start" in msg.topic:
    #     if lastTrig != 5:
    #         countSeg[5] += 1
    #         lastTrig = 5
    # if "lego/segment06/sensor/start" in msg.topic:
    #     if lastTrig != 6:
    #         countSeg[6] += 1
    #         lastTrig = 6
    # if "lego/segment07/sensor/start" in msg.topic:
    #     if lastTrig != 7:
    #         countSeg[7] += 1
    #         lastTrig = 7
    # if "lego/segment08/sensor/start" in msg.topic:
    #     if lastTrig != 8:
    #         countSeg[8] += 1
    #         lastTrig = 8
    # if "lego/segment09/sensor/start" in msg.topic:
    #     if lastTrig != 9:
    #         countSeg[9] += 1
    #         lastTrig = 9
    if printCounts:
        for car in range(numCars):
            print(str(idCars[car]) + ": " + str(countCars[car][0]) + " " + str(countCars[car][1]) + " " + str(countCars[car][2]))
        # time.sleep(4)
        # print("countSeg01 = " + str(countSeg01))
        # print("countSeg02 = " + str(countSeg02))
        # print("countSeg03 = " + str(countSeg03))
        # print("countSeg04 = " + str(countSeg04))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.1.1.50", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
