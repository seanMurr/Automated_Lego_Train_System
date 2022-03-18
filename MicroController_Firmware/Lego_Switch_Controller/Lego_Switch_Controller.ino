#include "WiFi.h"
#include <PubSubClient.h>
#include <ESP32Servo.h>

 
#define NUM_SERVOS 6

const char* ssid = "Lego_Train24";
const char* password =  "LegoTrain";

const char* mqtt_server = "192.168.0.10";

WiFiClient espClient;
PubSubClient client(espClient);

Servo myservos[8];  // create servo object to control a servo
// twelve servo objects can be created on most boards

int servoPins[8] = {13,12,14,27,26,25,33,32};

int servoPos[8] = {170,170,170,170,170,170,170,170};    // variable to store the servo position
// 140 to 175
int servoID[8] = {0,1,2,3,4,5,6,7};
char * servoTopic[8] = {"lego/track/switch/00",
                        "lego/track/switch/01",
                        "lego/track/switch/02",
                        "lego/track/switch/03",
                        "lego/track/switch/04",
                        "lego/track/switch/05",
                        "lego/track/switch/06",
                        "lego/track/switch/07"};

const int ledPin = LED_BUILTIN;
long lastMsg = 0;
 
void setup() {
 
  Serial.begin(115200);
  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  pinMode(ledPin, OUTPUT); 

  // attach NUM_SERVOS to each  
  for(int i=0;i<NUM_SERVOS;i++){ 
    myservos[i].attach(servoPins[i]);  // attaches the servo on pin 9 to the servo object
    myservos[i].write(servoPos[i]); // initial position
  }
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
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
  for(int i=0;i<NUM_SERVOS;i++){
    if (String(topic) == servoTopic[i]) {
      servoPos[i] = messageTemp.toInt();
      Serial.print("Changing output of ");
      Serial.print(i);
      Serial.print(" to ");
      Serial.println(servoPos[i]);
      myservos[i].write(servoPos[i]);
      delay(15);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESPTestinglient")) {
      Serial.println("connected");
      // Subscribe
      for(int i=0;i<NUM_SERVOS;i++){
        client.subscribe(servoTopic[i]);
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
    client.publish("lego/testing/switch/01", "connected");
  }
}
 
void loop() {
  if (!client.connected()) {
    reconnect();
    Serial.println("\nREADY!\n");
  }
  client.loop();

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
