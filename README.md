# Automated_Lego_Train_System
README.md

Project details can be found on the below Google Docs file.
https://docs.google.com/document/d/1lxXYNgJCgzpIqd5K40-fcvLhcOwaUo2JmRowEYo6z_Q/edit?usp=sharing

Current version is V1. Please use files in that folder.

An MQTT server/broker is required for this project to operate.

Python scripts are run on Raspberry Pi.

One or more ESP32's, running 'LEGO_PU_Serial_Multi_Control.ino' script, are connected to the Raspberry Pi via USB and provide communication to the LEGO Powered Up hubs. Each ESP32 can pair with up to 3 hubs.

Other ESP32's, running tracksensor_LED_tripwire.ino, are connected to LED LDR tripwires and define the end of a segment of track. One ESP32 can monitor multiple sensors if necessary. ESP32 track sensors send a message to Raspberry Pi, via MQTT broker, allowing Raspberry Pi to monitor the position of individual trains and control their motion.


********************************************************
PROBLEMS
********************************************************
Sensors are visible.
Sensors trigger multiple times due to the gaps through the train at the height of the bogies (ie wheel assembly).

********************************************************
SOLUTIONS
********************************************************
Use sensors that can be placed under the train track.
Hall Effect Sensors
Tried using hall effect sensors and magnets under each train however these were found to be unreliable. Tried multiple hall effect sensors to increase the detection field. This improved reliability however detection of a passing train was still to not reliable enough. Speed decreased the reliability remarkably.
