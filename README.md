# Automated_Lego_Train_System
README.md

Project details can be found on the below Google Docs file.
https://docs.google.com/document/d/1lxXYNgJCgzpIqd5K40-fcvLhcOwaUo2JmRowEYo6z_Q/edit?usp=sharing

Current version is V2. 

An MQTT server/broker is required for this project to operate.

Python scripts are run on Raspberry Pi.

One or more ESP32's, running 'LEGO_PU_Serial_Multi_Control.ino' script, are connected to the Raspberry Pi via USB and provide communication to the LEGO Powered Up hubs. Each ESP32 can pair with up to 3 hubs.

Other ESP32's, connected to a RFID reader, reads RFID tags attached to each train car. ESP32 track sensors send a message to Raspberry Pi, via MQTT broker, allowing Raspberry Pi to monitor the position of individual cars and control the motion of trains that can contain more than 1 engine.


********************************************************
PROBLEMS
********************************************************


********************************************************
SOLUTIONS
********************************************************
