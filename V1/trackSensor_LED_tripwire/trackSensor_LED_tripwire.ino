/****************************************************
 * tracksensor_LED_tripwire.ino
 * 
 * controller for sensors for lego train set
 * each sensor consists of an LED and a LDR
 * when the value from the LDR is below a threshold then the LDR can
 * 'see' the LED. When the LDR is above that threshold then there is a train in the way.
 * When the LDR value changes (low to high or high to low) then a specific MQTT message is sent.
 * This system can monitor a number of sensors. The number of sensors attached is specified in 
 * 'NUM_INDICATORS' and the sensor details are specified in the intiIndicators() function
 */

// headers required to connect to wifi network and mqtt
#include "WiFi.h"
#include <PubSubClient.h>

// system settings
#define NUM_INDICATORS 3    // number of sensors attached to this device
#define SIGNAL_PIN 2        // this is the onboard LED used indicate that at least 1 sensor beam  is currently broken
#define TRIGGER_DELAY 200   // used to reduce multiple triggers caused by gaps in train carrages allowing light to pass
#define TRIGGER_DEBOUNCE 20 // used to ensure that trigger events are caused by a train and not just a stray bug or electrical artifact
#define LIGHT_THRESHOLD 2000// the comparison value used to determine if LED light is blocked or not

// network and mqtt connection values
const char* ssid = "HO";
const char* password =  "5Acrewoods";
const char* mqtt_server = "10.1.1.50";

// wifi object
WiFiClient espClient;
// mqtt object
PubSubClient client(espClient);

// flag to show if any sensor beams are broken
boolean signal = false;

// arrays to hold sensor settings and state values
char* mqttID[NUM_INDICATORS];
uint8_t pin[NUM_INDICATORS];
unsigned long lastTrig[NUM_INDICATORS]; 
boolean currentTrigger[NUM_INDICATORS];
boolean currentState[NUM_INDICATORS];

// function type definitions
void callback(char* topic, byte* payload, unsigned int length);
void initIndicators(void);
void setup_wifi(void);
void setup_mqtt(void);
void reconnect(void);

// recieve message
void callback(char* topic, byte* payload, unsigned int length) {
  // this is blank as this device does not subscribe to any message topics
  // this function must be present even if unused
}


void setup() {
  // serial connection for debuging ans to see real time state of sensors
  Serial.begin(9600);
  
  // initialise network and mqtt
  setup_wifi();
  setup_mqtt();

  // initialise sensors
  initIndicators();

  // setup and initialise the
  pinMode(SIGNAL_PIN,OUTPUT);
  digitalWrite(SIGNAL_PIN,signal);
}

   

void loop() {
  // ************* this block is required for MQTT to work
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  //**************  all programming below this line

  // print the raw value for each sensor
  for(int i=0;i < NUM_INDICATORS;i++) {
    Serial.printf("%6i",analogRead(pin[i]));
  }
  
  
  // check each indicator and set currentTrigger
  for(int i=0;i < NUM_INDICATORS;i++) {
    if(analogRead(pin[i]) < LIGHT_THRESHOLD) {
      // sensor is clear ie no train here
      currentTrigger[i] = true;
    }else{
      // sensor is obscured ie there IS a train here
      currentTrigger[i] = false;
    }
  }
  
  // re-test to confirm trigger. wait a short period of time first
  delay(TRIGGER_DEBOUNCE);
  for(int i=0;i < NUM_INDICATORS;i++) {
    if(!currentTrigger[i] && (analogRead(pin[i]) > LIGHT_THRESHOLD)) {
      // there is definatly something large here. most probably a train
      currentTrigger[i] = false;
    }else{
      // no there is nothing here
      currentTrigger[i] = true;
    }
  }

  // print the current trigger value of each sensor
  for(int i=0;i < NUM_INDICATORS;i++) {
    Serial.printf("%6d",currentTrigger[i]);
  }
  
  // This is a new trigger if last trigger is more than TRIGGER_DELAY milliseconds ago
  for(int i=0;i < NUM_INDICATORS;i++) {
    if(currentTrigger[i] && !currentState[i]) {
      // trigger is current
      if(millis() - lastTrig[i] > TRIGGER_DELAY) {
        Serial.printf("%s %i"," Got here",i);
        // train is here
        client.publish(mqttID[i],"open");
        currentState[i] = true;
      }
      lastTrig[i] = millis();
    }
  }
  
  // if currentState is true ('closed') and currentTrigger is false ('open')
  // and TRIGGER_DELAY has passed since 'closed' was last read 
  // change state to 'open' and send 'open' signal
  for(int i=0;i < NUM_INDICATORS;i++) {
    if(!currentTrigger[i] && currentState[i]) {
      // check that TRIGGER_DELAY time has passed since last 'closed'event
      if(millis() - lastTrig[i] > TRIGGER_DELAY) {
        // train has passed
        client.publish(mqttID[i],"closed");
        currentState[i] = false;
      }
    }
  }
  
  signal = false;
  for(int i=0;i < NUM_INDICATORS;i++) {
    if(!currentTrigger[i]) {
      signal = true;
    }
  }
  digitalWrite(SIGNAL_PIN,signal);
  
  
  Serial.println();
}

void setup_wifi() {
  //
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    // print dots while not connected
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  // print IP address of device
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void setup_mqtt() {
  // setup the mqtt object
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  // connect to mqtt server
  reconnect();
}

void reconnect() {
  // check for connection to mqtt server
  while (!client.connected()) {
    // not connected so try to connect to mqtt server
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // when connecting the device must be given name that is not currently in use 
    // i.e. each device must have a unique name. as we are just testing, this will be fine
    if (client.connect("ESPSegmentSensors")) {
      Serial.println("connected");
      // send an mqtt message to prove connection
      client.publish("lego/testing", "ESPSegmentSensors Connected");
      // Subscribe - we are not subscribing to any topics but this is where and how it is done
//      client.subscribe("esp32/output");
    } else {
      // connection failed
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying to connect to mqtt
      delay(5000);
    }
  }
}

void initIndicators() {
  // initialise sensor for segment 0
  pin[0] = 36;
  mqttID[0] = "lego/train/segments/indicator/00";
  lastTrig[0] = 0;
  currentTrigger[0] = false;
  currentState[0] = false;
  
  // initialise sensor for segment 1
  pin[1] = 39;
  mqttID[1] = "lego/train/segments/indicator/01";
  lastTrig[1] = 0;
  currentTrigger[1] = false;
  currentState[1] = false;

  // initialise sensor for segment 2
  pin[2] = 34;
  mqttID[2] = "lego/train/segments/indicator/02";
  lastTrig[2] = 0;
  currentTrigger[2] = false;
  currentState[2] = false;

  // further sensors can be added.
  // just increase the array id 
  // make sure that "#define NUM_INDICATORS" represents the number of sensors listed
  // all sensors must have a unique pin and mqttID
}
