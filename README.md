# Automated_Lego_Train_System
README.md

Project details can be found on the below Google Docs file.
https://docs.google.com/document/d/1lxXYNgJCgzpIqd5K40-fcvLhcOwaUo2JmRowEYo6z_Q/edit?usp=sharing

Current version is V2.

An MQTT server/broker is required for this project to operate.

Python scripts are run on Raspberry Pi.

One or more ESP32's, running 'LEGO_PU_Serial_Multi_Control.ino' script, are connected to the Raspberry Pi via USB and provide communication to the LEGO Powered Up hubs. Each ESP32 can pair with up to 3 hubs.

Other ESP32's, connected to a RFID reader, reads RFID tags attached to each train car. ESP32 track sensors send a message to Raspberry Pi, via MQTT broker, allowing Raspberry Pi to monitor the position of cars and control the motion of trains that can contain more than 1 engine. A train of cars will be on more than one segment whilst transitioning from one segment to teh next. ie a train of 5 cars may have 3 cars on segment 00 and 2 cars on segment 01 at a particular moment in time.

Segments may have another segment listed as a sibling. This is for when 2 segments use a shared piece of track ie tracks crossing or some track switches.

Track switches activated by servo.

********************************************************
PROBLEMS
********************************************************
Problems with latency of MQTT. As more trains and cars are added to the tracks and more segments are added there is an large increase in mqtt messages being sent. On short segments the issue of the message of the first car leaving a segment occures before the message of the second car entering the segment is received. This causes the system to crash as the segment has no train when there is still a train physically on, and entering, the segment.

********************************************************
SOLUTIONS
********************************************************
Working on reimplementing with wires instead of a WiFi-mqtt solution.
