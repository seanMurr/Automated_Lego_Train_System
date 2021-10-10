#!/usr/bin/env python3
import time
from cars import Car, Engine
from Train import Train
from Segment import Segment
import paho.mqtt.client as mqttClient

mqttServerAddress = "10.1.1.50"

# setup system
trackSegments = []
trains = []
cars = []
# start = True

def main():

    createObjects()

    # prompt for all engines to be turned on and connected
    for car in cars:
        if isinstance(car, Engine):
            input("Connect " + car.name +" engine and press enter")

    # create an MQTT client and attach routines to it.
    client = mqttClient.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(client.connect(mqttServerAddress, 1883, 60))
    # time.sleep(10)
    # cars[0].set_Speed(30)
    # time.sleep(13.5)
    # cars[0].set_Speed(0)
    # Process network traffic and dispatch callbacks. This will also handle
    # reconnecting. Check the documentation at
    # https://github.com/eclipse/paho.mqtt.python
    # for information on how to use other loop*() functions
    # client.loop_forever()

    # if start is True then tell segment[0] to send train.
    trackSegments[2].sendTrain()

    start = False

    run = True
    while run:
        client.loop()

def createObjects():
    # create track segments
    print("******Creating Track Segments******")
    trackSegments.append(Segment(0,"Seg00",144,None,0,None,0,"lego/train/segments/indicator/00",None,0,40))
    trackSegments.append(Segment(1,"Seg01",144,None,0,None,0,"lego/train/segments/indicator/01",None,0,40))
    trackSegments.append(Segment(2,"Seg02",144,None,0,None,0,"lego/train/segments/indicator/02",None,0,40))


    # attach track segments together
    print("******Connecting Track Segments******")
    # outside loop
    trackSegments[0].getSet_nextSegment(trackSegments[1])
    trackSegments[0].getSet_prevSegment(trackSegments[2])
    trackSegments[1].getSet_nextSegment(trackSegments[2])
    trackSegments[1].getSet_prevSegment(trackSegments[0])
    trackSegments[2].getSet_nextSegment(trackSegments[0])
    trackSegments[2].getSet_prevSegment(trackSegments[1])

    # create cars
    print("*****Creating cars******")
    # 0
    cars.append(Engine("002","ResPass 1a",50,True,True,True,("engine","passanger"),
                    "90:84:2b:01:a7:3a","/dev/ttyUSB0","0",(1,0)))
    # 1
    cars.append(Engine("001","Green Cargo 1a",50,True,True,True,("engine","cargo"),
                    "90:84:2b:07:b8:83","/dev/ttyUSB0","2",(-1,1)))



    # create trains
    print("******Creating Trains******")
    trains.append(Train([cars[0]],0,1))
    trains.append(Train([cars[1]],0,1))

    # # locate trains on track
    print("******Placing trains onto tracksegments******")
    trackSegments[1].train = trains[0]
    trackSegments[1].numCars = len(trains[0].cars)
    trackSegments[2].train = trains[1]
    trackSegments[2].numCars = len(trains[1].cars)

    # output setup to screen
    for segment in trackSegments:
        segment.print()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lego/#")
    # client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # output each mqtt message
    # print("****"+msg.topic+" "+str(msg.payload))

    # compare msg.topic to mqttName of each track indicator
    if "segments/indicator" in msg.topic:
        print("Looking for " + msg.topic +" in tracks")
        for segment in trackSegments:
            # print("Checking segment: "+ segment.getSet_microId())
            # check that endIndicator exists
            if segment.getSet_microId() is not None:
                # compare topic to endIndicator
                if segment.getSet_microId() in msg.topic:
                    print("Received " + str(msg.payload.decode('utf-8')) +" from segment "+str(segment.getSet_id()))
                    segment.processMessage(msg.topic, msg.payload.decode('utf-8'))
                    # track.activateSegEndIndicator(msg.payload)


try:
    print("*************************")
    print("*********begin***********")
    main()
except KeyboardInterrupt:
    print("Exiting gracefully")
except Exception as ex:
    print("****************   ERROR   ****************************")
    print(ex)
finally:
    print("Stopping trains ")
    for train in trains:
        # print("stopping train ")
        train.getSet_speed(0)

print("********finished*********")
print("*************************")
# output system to screen
for segment in trackSegments:
    segment.print()
    print()
