#include <WiFi.h>
#include <PubSubClient.h>
#include <esp_timer.h>
 
const char* ssid = "dvorak";
const char* password =  "Hlavni115";
const char* mqttServer = "192.168.82.87";
const int mqttPort = 1883;
const char* mqttUser = "yourMQTTuser";
const char* mqttPassword = "yourMQTTpassword";

const int batPin = 36;
const int temperPin = 39;
const int measurePin = 22;
const int averaging = 100;

WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
  pinMode(measurePin, OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqttServer, mqttPort);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

int lastPublish = 0;
int milisecondsSinceBoot;
int pubInterval = 1000;
char msg[1024];
void loop() {
  milisecondsSinceBoot = esp_timer_get_time() / 1000;
  if ((milisecondsSinceBoot - lastPublish) > pubInterval) {
    lastPublish = milisecondsSinceBoot;

    snprintf(msg, 1024, "{ \"battery\": %d, \"temperature\": %d }", measurement_bat(), measurement_temper());

    client.publish("esp/test", msg);
  }
  client.loop();
}

int measurement_bat(){
  digitalWrite(measurePin,HIGH);

  int batValue = 0;
  for (int i=0; i < averaging; i++) {
    batValue = batValue + analogRead(batPin);
  }
  batValue = batValue/averaging;
  return batValue;
}

int measurement_temper() {
  int temperValue = 0;
  for (int i=0; i < averaging; i++) {
    temperValue = temperValue + analogRead(temperPin);
  }
  temperValue = temperValue/averaging;
  return temperValue;
}