/**
 * Listen to serial port (115200)
 * To set speed of a connected hub send following via serial
 * 1,hubId,speed      eg 1,0,100  to set speed of hub '0' to maximum
 * 
 * To set up a hub send the following seperate messages
 * 0                  enter train settings
 * 0                  the id of the train to set 0, 1, or 2
 * 00:11:22:33:44:55  the bluetooth idof the hub
 * name               the human readable description of the engine
 * 1,0                the direction of the 2 motors (A B) 1 is forward, -1 is backwards, 0 is no motor in that port
 * 
 */

#include "Lpf2Hub.h"
#define MAX_NUM_HUBS 3
int const numHubs = 3;

// arrays to hold hub properties
char id[MAX_NUM_HUBS][18];
char desc[MAX_NUM_HUBS][20];
int port[MAX_NUM_HUBS][2];

// create array of hub instances
Lpf2Hub puHub[MAX_NUM_HUBS];
byte puPort[2] = {(byte)PoweredUpHubPort::A,(byte)PoweredUpHubPort::B};

// serial communications variables
int comHub, comSpd, comFunc,comId;
char comBt[18];
void setup() {
  Serial.begin(115200);
  delay(4000);
  for (int i=0;i<numHubs;i++) {
    strcpy(id[i],"");
    strcpy(desc[i],"");
    port[i][0]= 0;
    port[i][1]= 0;
  }

  
  printHubs();
}

void loop() {
  // check if hubs are connected
  if(millis()%1000 == 0) {
    connectHubs();
  }

  // print hub status
  if(millis()%10000 == 0) {
    printHubs();
  }

  // if there's any serial available, read it:
  while (Serial.available() > 0) {
    comFunc = Serial.parseInt();
    if (comFunc == 0) {
      // setting train settings
      Serial.println("Setting train settings");
      readEndOfLine();
      // wait for id
      Serial.println("Waiting for engine ID");
      while (!Serial.available()) {}
      comId = Serial.parseInt();
      readEndOfLine();
      // wait for address
      Serial.println("Waiting for bluetooth address");
      while (!Serial.available()) {}
      Serial.readBytesUntil('\n',id[comId],17);
      Serial.println(id[comId]);
      readEndOfLine();
      // wait for desc
      Serial.println("Waiting for engine description");
      while (!Serial.available()) {}
      strcpy(desc[comId],"");
      Serial.readBytesUntil('\n',desc[comId],20);
      Serial.println(desc[comId]);
      // set motors 
      Serial.println("Waiting for motor A direction");
      while (!Serial.available()) {}
      port[comId][0] = Serial.parseInt();
      port[comId][1] = Serial.parseInt();
      readEndOfLine();
      printHubs();
    }else {
      comHub = Serial.parseInt();
      comSpd = Serial.parseInt();
      readEndOfLine();
    }
  
    // send command to hub
    // check data is valid
    // check comHub is a valid puHub
    if(comHub >= 0 && comHub < numHubs) {
      // check that puHub[comHub] is connected
      if(puHub[comHub].isConnected()){
        // check speed is within range -100 to 100
        if(comSpd >= -100 && comSpd <= 100) {
          for(int p=0;p<2;p++){
            //check port has a motor
            if(port[comHub][p] !=0) {
              //check if speed is not 0
              if(comSpd != 0) {
                // multiply comSpd by port value to reverse direction of backward 
                // facing motors
                puHub[comHub].setBasicMotorSpeed(puPort[p], comSpd*port[comHub][p]);
              }else {
                puHub[comHub].stopBasicMotor(puPort[p]);
              }
            }
          }
          Serial.printf("%s speed set to %d\n",desc[comHub],comSpd);
        }
      }
    }
  }
//  delay(2);
//  printHubs();
}

/**
 * loop through all puHubs and connect if not currently connected.
 * output to serial details of new connections
 */
void connectHubs() {
  for (int i=0;i<numHubs;i++) {
    if (strcmp(id[i], "") !=0) {
      if (!puHub[i].isConnected() && !puHub[i].isConnecting()) {
        // myTrainHub.init(); // initialise the PoweredUpHub instance
  //      char sub[17];
  //      strncpy(sub, id[i], 17);
        Serial.printf("Attempting to connect to hub at: %s\n",id[i]);
        puHub[i].init(id[i]); //example of initialising an hub with a specific address
        delay(20);
        
      }
      if (puHub[i].isConnecting()) {
        puHub[i].connectHub();
        if (puHub[i].isConnected()) {
          // set name of puHub[]
          puHub[i].setHubName(desc[i]);
          Serial.printf("Connected to HUB: %d\n",i);
          Serial.printf("Hub address: %s\n",puHub[i].getHubAddress().toString().c_str());
          Serial.printf("Hub name: %s\n",puHub[i].getHubName().c_str());
        } else {
          Serial.printf("Failed to connect to HUB: %d\n",i);
          puHub[i].connectHub();
        }
      }
    }
    delay(10);
  }
}

/**
 * print to serial details of hubs and their connection status
 */
void printHubs(){
  Serial.printf("\n\nNumber of Hubs: %d\n",numHubs);
  for(int i=0;i<numHubs;i++) {
    Serial.printf("\nHub: %d\n",i);
    Serial.printf("desc: %s\n",desc[i]);
    Serial.printf("ID: %s\n",id[i]);
    Serial.printf("PortA: %d\n",port[i][0]);
    Serial.printf("PortB: %d\n",port[i][1]);
    Serial.print("Status: ");
    if(puHub[i].isConnected()) {
      Serial.println("Connected");
    } else {
      if(puHub[i].isConnecting()) {
        Serial.println("Connecting");
      }else {
        Serial.println("NOT connected");
      }
    }
  }
}
/**
 * read serial to end of line '\n'
 */
void readEndOfLine(){
  while (Serial.read() != '\n'){}
}
