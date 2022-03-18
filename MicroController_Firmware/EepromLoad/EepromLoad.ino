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
  inEeprom.begin("lego_train",false); // namespace
}

void loop() {
  clearLocalData();
  loadFromEeprom();

  displayData("CURRENT EEPROM DATA");
  
  input = getStringFromSerial("Do you want to update the current data Y/N");
  if(input == "Y" || input == "y") {
    data.ssid = "Lego_Train24"; //getStringFromSerial("Enter the WiFi ssid");
    Serial.println(data.ssid);
    data.password = "LegoTrain"; //getStringFromSerial("Enter the WiFi password");
    Serial.println(data.password);
    data.mqtt_server = "192.168.0.10"; //getStringFromSerial("Enter the mqtt_server address");
    Serial.println(data.mqtt_server);
    data.segmentID = getStringFromSerial("Enter the segmentID for this device");
    Serial.println(data.segmentID);

    displayData("CURRENT STORED DATA");
    input = getStringFromSerial("Do you want to store these new values Y/N");
    if(input == "Y" || input == "y") {
      // clear current Eeprom 'lego_train' values
      inEeprom.clear();
      saveToEeprom();
    }
  }
}

void loadFromEeprom() {
  data.ssid = inEeprom.getString("ssid", "NULL");
  data.password = inEeprom.getString("password", "NULL");
  data.mqtt_server = inEeprom.getString("mqtt_server", "NULL");
  data.segmentID = inEeprom.getString("segmentID", "NULL");
}

void saveToEeprom() {
  inEeprom.putString("ssid", data.ssid);
  inEeprom.putString("password", data.password);
  inEeprom.putString("mqtt_server", data.mqtt_server);
  inEeprom.putString("segmentID", data.segmentID);
  Serial.println("New values stored in Eeprom\n");
}

void displayData(char* msg) {
  Serial.printf("\n\n  ** %s **\n",msg);
  Serial.printf("%-13s ","ssid");
  Serial.println(data.ssid);
  Serial.printf("%-13s ","password");
  Serial.println(data.password);
  Serial.printf("%-13s ","mqtt_server");
  Serial.println(data.mqtt_server);
  Serial.printf("%-13s ","segmentID");
  Serial.println(data.segmentID);
  Serial.println();  
//  Serial.println(data.ssid);
//  Serial.println(data.password);
//  Serial.println(data.mqtt_server);
//  Serial.println(data.segmentID);
//  Serial.println();
}
void clearLocalData() {
  data.ssid = "";
  data.password = "";
  data.mqtt_server = "";
  data.segmentID = "";
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
