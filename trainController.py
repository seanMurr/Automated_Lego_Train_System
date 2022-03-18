#!/usr/bin/env python3
import time
from cars import Car, Engine
from Train import Train
from Segment import Segment
import paho.mqtt.client as mqttClient

mqttServerAddress = "192.168.0.10"

# setup system
trackSegments = []
trains = []
cars = []
# start = True

def main():

    createObjects()

    # prompt for all engines to be turned on and connected
    print("\n\nMake sure the following engine hubs are connected\n")
    for car in cars:
        if isinstance(car, Engine):
            print(car.name)
    input("\nPress Enter to START\n")

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
    trackSegments[0].shortPrint()
    # Tell each segment to send train if it has one and track is clear.
    trackSegments[0].sendTrain()

    start = False

    run = True
    while run:
        client.loop()

def createObjects():
    # create track segments
    print("******Creating Track Segments******")
    trackSegments.append(Segment(0,"Seg00",90,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/00",None,0,40))
    trackSegments.append(Segment(1,"Seg01",128,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/01",None,0,40))
    trackSegments.append(Segment(2,"Seg02",160,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/02",None,0,40))
    trackSegments.append(Segment(3,"Seg03",112,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/03",None,0,40))
    trackSegments.append(Segment(4,"Seg04",144,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/04",None,0,40))
    trackSegments.append(Segment(5,"Seg05",208,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/05",None,0,40))
    trackSegments.append(Segment(6,"Seg06",272,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/06",None,0,40))
    trackSegments.append(Segment(7,"Seg07",80,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/07",None,0,40))
    trackSegments.append(Segment(8,"Seg08",160,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/08",None,0,40))
    trackSegments.append(Segment(9,"Seg09",144,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/09",None,0,40))
    trackSegments.append(Segment(10,"Seg10",144,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/10",None,0,40))
    trackSegments.append(Segment(11,"Seg11",240,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/11",None,0,40))
    trackSegments.append(Segment(12,"Seg12",288,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/12",None,0,40))
    trackSegments.append(Segment(13,"Seg13",224,[None],None,[0],0,[None],None,[0],0,"lego/train/segments/indicator/13",None,0,40))

    for segment in trackSegments:
        print(segment.getSet_desc())
    # attach track segments together
    print("******Connecting Track Segments******")
    # inside loop
    trackSegments[0].set_nextSegment(trackSegments[1],0)
    trackSegments[0].set_prevSegment(trackSegments[6],0)
    trackSegments[1].set_nextSegment(trackSegments[2],0)
    trackSegments[1].set_prevSegment(trackSegments[0],0)
    trackSegments[2].set_nextSegment(trackSegments[3],0)
    trackSegments[2].set_prevSegment(trackSegments[1],0)
    trackSegments[3].set_nextSegment(trackSegments[4],0)
    trackSegments[3].set_prevSegment(trackSegments[2],0)
    trackSegments[4].set_nextSegment(trackSegments[5],0)
    trackSegments[4].set_prevSegment(trackSegments[3],0)
    trackSegments[5].set_nextSegment(trackSegments[7],0)
    trackSegments[5].set_prevSegment(trackSegments[4],0)
    # outside loop
    trackSegments[6].set_nextSegment(trackSegments[0],0)
    trackSegments[6].set_prevSegment(trackSegments[13],0)
    trackSegments[7].set_nextSegment(trackSegments[8],0)
    trackSegments[7].set_prevSegment(trackSegments[5],0)
    trackSegments[8].set_nextSegment(trackSegments[9],0)
    trackSegments[8].set_prevSegment(trackSegments[7],0)
    trackSegments[9].set_nextSegment(trackSegments[10],0)
    trackSegments[9].set_prevSegment(trackSegments[8],0)
    trackSegments[10].set_nextSegment(trackSegments[11],0)
    trackSegments[10].set_prevSegment(trackSegments[9],0)
    trackSegments[11].set_nextSegment(trackSegments[12],0)
    trackSegments[11].set_prevSegment(trackSegments[10],0)
    trackSegments[12].set_nextSegment(trackSegments[13],0)
    trackSegments[12].set_prevSegment(trackSegments[11],0)
    trackSegments[13].set_nextSegment(trackSegments[6],0)
    trackSegments[13].set_prevSegment(trackSegments[12],0)

    # crossover: set sibling segments
    trackSegments[0].getSet_siblingSegment(trackSegments[7])
    trackSegments[7].getSet_siblingSegment(trackSegments[0])

    # create cars
    print("*****Creating cars******")
    # 0
    cars.append(Engine("002","RedPass 1a",30,True,True,True,("engine","passanger"),
                    "90:84:2b:01:a7:3a","/dev/ttyUSB0","0",(1,0),40))

    # 1
    cars.append(Engine("001","Green Cargo 1a",34,True,True,True,("engine","cargo"),
                    "90:84:2b:07:b8:83","/dev/ttyUSB0","2",(-1,1),35))
    # 2
    cars.append(Car("101","RedPassC101",26,True,True,True,("passanger")))
    # 3
    cars.append(Car("102","WhitePasC102",26,True,True,True,("passanger")))
    # 4
    cars.append(Engine("003","RedPass 1b",30,True,True,True,("engine","passanger"),
                    "90:84:2b:19:2c:22","/dev/ttyUSB0","1",(-1,0),40))
    # 5
    cars.append(Engine("004","WhitePass 1a",36,True,True,True,("engine","passanger"),
                    "90:84:2b:be:49:08","/dev/ttyUSB1","0",(1,0),40))
    # 6
    cars.append(Engine("004","WhitePass 1b",36,True,True,True,("engine","passanger"),
                    "90:84:2b:09:6b:88","/dev/ttyUSB1","1",(-1,0),40))
    # 7
    cars.append(Car("103","WhitePasC103",26,True,True,True,("passanger")))
    # 8
    cars.append(Engine("005","Mearsk 1b",40,True,True,True,("engine","cargo"),
                    "90:84:2b:21:db:7d","/dev/ttyUSB1","2",(1,-1),35))
    # 9
    cars.append(Car("104","FreightC104",36,True,True,True,("cargo")))
    # 10
    cars.append(Car("105","FreightC105",36,True,True,True,("cargo")))
    # 11
    cars.append(Engine("006","BluePass 1a",34,True,True,True,("engine","passanger"),
                    "90:84:2b:15:e1:7c","/dev/ttyUSB2","0",(1,0),40))
    # 12
    cars.append(Engine("007","BluePass 1b",34,True,True,True,("engine","passanger"),
                    "90:84:2b:1d:56:25","/dev/ttyUSB2","1",(-1,0),40))

    # create trains
    print("******Creating Trains******")
    # 0 Red Passanger 1
    trains.append(Train([cars[0],cars[4]],0,1))
    # 1 Green Cargo 1
    trains.append(Train([cars[1],cars[3]],0,1))
    # 2 White Passanger 1
    trains.append(Train([cars[5],cars[6]],0,1))
    # 3 Mearsk Cargo 1
    trains.append(Train([cars[8],cars[10]],0,1))

    # # locate trains on track
    print("******Placing trains onto tracksegments******")
    trackSegments[1].train = trains[0]
    trackSegments[1].numCars = len(trains[0].cars)
    trackSegments[5].train = trains[1]
    trackSegments[5].numCars = len(trains[1].cars)
    trackSegments[8].train = trains[2]
    trackSegments[8].numCars = len(trains[2].cars)
    trackSegments[13].train = trains[3]
    trackSegments[13].numCars = len(trains[3].cars)

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
    # output short segment map
    trackSegments[0].shortPrint()
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

# output short segment map
trackSegments[0].shortPrint()
