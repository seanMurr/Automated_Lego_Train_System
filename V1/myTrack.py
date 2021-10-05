
import paho.mqtt.client as mqtt
import Segment
import Train
import time

mqttServerAddress = "10.1.1.50"

# setup system
tracks = []
trains = []

def main():

    createObjects(tracks, trains)

    # prompt for all engines to be turned on and connected
    for train in trains:
        input("Connect " + train.name +" engine and press enter")

    # everything else is handled by mqtt calls

    # Create an MQTT client and attach our routines to it.
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(client.connect(mqttServerAddress, 1883, 60))

    # tell each segment to send its train.
    # segment will only send a train if it has one
    # and the next segment is clear

    for segment in tracks:
        segment.sendTrain()

    # loop forever just processing MQTT medssages
    run = True
    while run:
        client.loop()

def createObjects(tracks,trains):
    # create tracks
    tracks.append(Segment.Segment("00",None,None,None,None,35,90,None,"lego/train/segments/indicator/00",None,mqttServerAddress))
    tracks.append(Segment.Segment("01",None,None,None,None,100,120,None,"lego/train/segments/indicator/01",None,mqttServerAddress))
    tracks.append(Segment.Segment("02",None,None,None,None,120,140,None,"lego/train/segments/indicator/02",None,mqttServerAddress))

    # attach tracks together
    tracks[0].getNextSegment(tracks[1])
    tracks[0].getPrevSegment(tracks[2])
    tracks[1].getNextSegment(tracks[2])
    tracks[1].getPrevSegment(tracks[0])
    tracks[2].getNextSegment(tracks[0])
    tracks[2].getPrevSegment(tracks[1])


    # create trains
    trains.append(Train.Train("passanger00",1,0,30,"90:84:2b:01:a7:3a","/dev/ttyUSB0","0",(1,0)))
    trains.append(Train.Train("cargo00",1,0,30,"90:84:2b:07:b8:83","/dev/ttyUSB0","2",(-1,1)))
    # locate trains on segments
    tracks[2].train = trains[0]
    tracks[1].train = trains[1]

    # output system to screen
    for track in tracks:
        track.print()
        print()

# The callback for when the MQTT client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lego/train/#")
    # client.subscribe("#")

# The callback for when a MQTT PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # compare msg.topic to mqttName of each track indicator
    if "lego/train/segments/indicator" in msg.topic:
        print("Looking for " + msg.topic +" in tracks")
        for segment in tracks:
            # print("Checking track: "+track.getName())
            # check that endIndicator exists
            if segment.getSegEndIndicator() is not None:
                # compare topic to endIndicator
                if msg.topic == segment.getSegEndIndicator():
                    print("Sending " + str(msg.payload) +" to segment "+segment.getName())
                    segment.activateSegEndIndicator(msg.payload)
            if segment.getSegStartIndicator() is not None:
                # compare topic to startIndicator
                if msg.topic == segment.getSegStartIndicator():
                    segment.activateSegStartIndicator(msg.payload)


try:
    print("*************************")
    print("*********begin***********")
    main()
except KeyboardInterrupt:
    print("Exiting gracefully")
except Exception as ex:
    print(ex)
finally:
    print("Stopping trains ")
    for train in trains:
        print("stopping train " + train.getName())
        train.setSpeed(0)

print("********finished*********")
print("*************************")
# output system to screen
for track in tracks:
    track.print()
    print()
