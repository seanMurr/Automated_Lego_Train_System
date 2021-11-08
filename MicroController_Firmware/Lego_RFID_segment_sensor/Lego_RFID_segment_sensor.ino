/* Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    ESP32            Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3                     Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         22               RST
 * SPI SS      SDA(SS)      10            53        D10        5                10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        23               16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        19               14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        18               15
 */

#include <SPI.h>
#include <MFRC522.h>
#include "WiFi.h"
#include <PubSubClient.h>
#include <Preferences.h>

// esp32
#define SS_PIN 5
#define RST_PIN 22

struct setup {
  String ssid;
  String password;
  String mqtt_server;
  String segmentID;
  String mqtt_name;
  String mqtt_reconnect_topic;
  String mqtt_reconnect_msg;
  String mqtt_topic;
}setup_data;

//const char* ssid = "HO";
//const char* password =  "5Acrewoods";
//const char* mqtt_server = "10.1.1.50";
//const char* mqtt_name = "segment05";
//const char* mqtt_reconnect_topic = "lego/testing/segment05";
//const char* mqtt_reconnect_msg = "segment05 Connected";
//const char* mqtt_topic = "lego/train/segments/indicator/05";

char topic[40];
char msg[30];

// stress test variables
//const int maxIds = 4;
//int numIds = 0;
//char ids[maxIds][9];
//int count[maxIds] = {0,0,0,0};


Preferences inEeprom;
WiFiClient espClient;
PubSubClient client(espClient);
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

const int ledPin = LED_BUILTIN;
long lastMsg = 0;
// Init array that will store new NUID of RFID card
byte nuidPICC[4];
 
void setup() {
 
  Serial.begin(115200);
  inEeprom.begin("lego_train"); // namespace
  
  setup_env();
  setup_wifi();
  setup_mqtt();
  delay(50);
  setup_rfid();

  pinMode(ledPin, OUTPUT); 
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  while(read_rfid()) {
    // successful read of new token
    // send token via mqtt
    char uuidBuffer[9] = "";
    array_to_string(rfid.uid.uidByte,rfid.uid.size,uuidBuffer);
    Serial.println(uuidBuffer);
    client.publish(setup_data.mqtt_topic.c_str(), uuidBuffer);

//    stressTest(uuidBuffer);
    
  }

//  long now = millis();
//  if (now - lastMsg > 5000) {
//    lastMsg = now;
//    
//    // Convert the value to a char array
//    char nowString[16];
//    dtostrf(now, 1, 0, nowString);
//    Serial.print("Now: ");
//    Serial.println(nowString);
//    client.publish("lego/testing", nowString);
//
//  }
}

boolean read_rfid() {
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return false;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return false;

  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&  
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return false;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] || 
    rfid.uid.uidByte[1] != nuidPICC[1] || 
    rfid.uid.uidByte[2] != nuidPICC[2] || 
    rfid.uid.uidByte[3] != nuidPICC[3] ) {
    Serial.println(F("A new card has been detected."));

    // Store NUID into nuidPICC array
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
   
    Serial.println(F("The NUID tag is:"));
    Serial.print(F("In hex: "));
    printHex(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
    Serial.print(F("In dec: "));
    printDec(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
  }
  else {
    Serial.println(F("Card read previously."));
    // Halt PICC
    rfid.PICC_HaltA();
    return false;
  }

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
  return true;
}

void setup_mqtt() {
  client.setServer(setup_data.mqtt_server.c_str(), 1883);
  client.setCallback(callback);
}

void setup_rfid() {
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println(F("This code scan the MIFARE Classsic NUID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(setup_data.ssid); //ssid);

  WiFi.begin(setup_data.ssid.c_str(), setup_data.password.c_str());

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup_env() {
  //struct setup setup_data;
  setup_data.ssid = inEeprom.getString("ssid", "NULL");
  setup_data.password =  inEeprom.getString("password", "NULL");
  setup_data.mqtt_server = inEeprom.getString("mqtt_server", "NULL");
  setup_data.segmentID = inEeprom.getString("segmentID", "NULL");
  setup_data.mqtt_name = "segment"+setup_data.segmentID;
  setup_data.mqtt_reconnect_topic = "lego/testing/" + setup_data.mqtt_name; //segment05";
//  setup_data.mqtt_reconnect_msg = "segment05 Connected";
  setup_data.mqtt_topic = "lego/train/segments/indicator/" + setup_data.segmentID;
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
//  if (String(topic) == "esp32/output") {
//    Serial.print("Changing output to ");
//    if(messageTemp == "on"){
//      Serial.println("on");
//      digitalWrite(ledPin, HIGH);
//    }
//    else if(messageTemp == "off"){
//      Serial.println("off");
//      digitalWrite(ledPin, LOW);
//    }
//  }
}

void reconnect() {
  
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("\nAttempting MQTT connection...");
    // Attempt to connect
    if (client.connect(setup_data.mqtt_name.c_str())) {
      Serial.println("connected");
      client.publish(setup_data.mqtt_reconnect_topic.c_str(), (setup_data.mqtt_name + " Connected").c_str());
      // Subscribe
//      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// store a byte array into a char buffer as char representations
void array_to_string(byte array[], unsigned int len, char buffer[]) {
  for (unsigned int i = 0; i < len; i++)
  {
    byte nib1 = (array[i] >> 4) & 0x0F;
    byte nib2 = (array[i] >> 0) & 0x0F;
    buffer[i*2+0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
    buffer[i*2+1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
  }
  buffer[len*2] = '\0';
}


/**
 * Helper routine to dump a byte array as hex values to Serial. 
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

/**
 * Helper routine to dump a byte array as dec values to Serial.
 */
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}
