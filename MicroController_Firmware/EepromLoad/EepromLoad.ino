#include <Preferences.h>

Preferences inEeprom;

struct Data {
  String ssid;
  String password;
  String mqtt_server;
  String segmentID;
}data;

String input;

void setup() {
  Serial.begin(115200);
  inEeprom.begin("lego_train"); // namespace
}

void loop() {
  loadFromEeprom();

  displayData("CURRENT EEPROM DATA");
  
  input = getStringFromSerial("Do you want to update the current data Y/N");
  if(input == "Y" || input == "y") {
    data.ssid = getStringFromSerial("Enter the WiFi ssid");
    data.password = getStringFromSerial("Enter the WiFi password");
    data.mqtt_server = getStringFromSerial("Enter the mqtt_server address");
    data.segmentID = getStringFromSerial("Enter the segmentID for this device");

    displayData("CURRENT STORED DATA");
    input = getStringFromSerial("Do you want to store these new values Y/N");
    if(input == "Y" || input == "y") {
      // clear current Eeprom 'lego_train' values
      inEeprom.clear();
      saveFromEeprom();
    }
  }
}

void loadFromEeprom() {
  data.ssid = inEeprom.getString("ssid", "NULL");
  data.password = inEeprom.getString("password", "NULL");
  data.mqtt_server = inEeprom.getString("mqtt_server", "NULL");
  data.segmentID = inEeprom.getString("segmentID", "NULL");
}

void saveFromEeprom() {
  inEeprom.putString("ssid", data.ssid);
  inEeprom.putString("password", data.password);
  inEeprom.putString("mqtt_server", data.mqtt_server);
  inEeprom.putString("segmentID", data.segmentID);
  Serial.println("New values stored in Eeprom\n");
}

void displayData(char* msg) {
  Serial.printf("\n\n  ** %s **\n",msg);
  Serial.printf("%-13s %s\n","ssid", data.ssid);
  Serial.printf("%-13s %s\n","password", data.password);
  Serial.printf("%-13s %s\n","mqtt_server", data.mqtt_server);
  Serial.printf("%-13s %s\n","segmentID", data.segmentID);
  Serial.println();  
}

String getStringFromSerial(char* msg) {
  String result;
  Serial.println(msg);
  // wait for serial
  while (!Serial.available()){}
  
  while (Serial.available() > 0) {
    result = Serial.readString();
  }
   result.trim();
   return result;
}
