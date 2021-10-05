#!/usr/bin/env python3
import time
from cars import Car, Engine
import Train
from trackSegment import Segment
import paho.mqtt.client as mqttClient

mqttServerAddress = "10.1.1.50"

train = Train.Train([],0,1)

if isinstance(train,Train.Train):
    print("train is a valid Train")
else:
    print("train is invalid")
