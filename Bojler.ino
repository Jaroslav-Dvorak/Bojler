
// base class GxEPD2_GFX can be used to pass references or pointers to the display instance as parameter, uses ~1.2k more code
// enable or disable GxEPD2_GFX base class
#define ENABLE_GxEPD2_GFX 0

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <Fonts/FreeMonoBold24pt7b.h>
//////////////////////////////////////
#include <OneWire.h>
#include <DallasTemperature.h>
///////////////////////////////////
#include "defines.h"
int status = WL_IDLE_STATUS;     // the Wifi radio's status
#include <MQTTPubSubClient_Generic.h>

#define MQTT_SERVER         "192.168.43.37"
#define MQTT_PORT             1883
WiFiClient client;
MQTTPubSubClient mqttClient;

// ESP32 SS=5,SCL(SCK)=18,SDA(MOSI)=23,BUSY=15,RST=2,DC=0

// 2.13'' EPD Module
GxEPD2_BW<GxEPD2_213_BN, GxEPD2_213_BN::HEIGHT> display(GxEPD2_213_BN(/*CS=5*/ 5, /*DC=*/ 21, /*RST=*/ 2, /*BUSY=*/ 15)); // DEPG0213BN 122x250, SSD1680
//GxEPD2_3C<GxEPD2_213_Z98c, GxEPD2_213_Z98c::HEIGHT> display(GxEPD2_213_Z98c(/*CS=5*/ 5, /*DC=*/ 0, /*RST=*/ 2, /*BUSY=*/ 15)); // GDEY0213Z98 122x250, SSD1680

// 2.9'' EPD Module
//GxEPD2_BW<GxEPD2_290_BS, GxEPD2_290_BS::HEIGHT> display(GxEPD2_290_BS(/*CS=5*/ 5, /*DC=*/ 0, /*RST=*/ 2, /*BUSY=*/ 15)); // DEPG0290BS 128x296, SSD1680
//GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(GxEPD2_290_C90c(/*CS=5*/ 5, /*DC=*/ 21, /*RST=*/ 2, /*BUSY=*/ 15)); // GDEM029C90 128x296, SSD1680

///////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////

#define uS_TO_S_FACTOR 1000000ULL  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  60

void printWifiStatus()
{
  // print the SSID of the network you're attached to:
  // you're connected now, so print out the data
  Serial.print(F("You're connected to the network, IP = "));
  Serial.println(WiFi.localIP());

  Serial.print(F("SSID: "));
  Serial.print(WiFi.SSID());

  // print the received signal strength:
  int32_t rssi = WiFi.RSSI();
  Serial.print(F(", Signal strength (RSSI):"));
  Serial.print(rssi);
  Serial.println(F(" dBm"));
}

void setup()
{
  display.init(115200, true, 0, false);
  const int DS18B20pin = 14;
  OneWire oneWireDS(DS18B20pin);
  DallasTemperature senzoryDS(&oneWireDS);

  uint16_t box_x = 10;
  uint16_t box_y = 10;
  uint16_t box_w = 230;
  uint16_t box_h = 102;
  uint16_t cursor_y = box_y + box_h - 30;
  if (display.epd2.WIDTH < 104) cursor_y = box_y + 6;
  uint16_t incr = display.epd2.hasFastPartialUpdate ? 1 : 3;
  display.setFont(&FreeMonoBold24pt7b);
  display.setTextSize(2);
  if (display.epd2.WIDTH < 104) display.setFont(0);
  display.setTextColor(GxEPD_BLACK);
  display.firstPage();
  do
  {
    display.fillRect(box_x, box_y, box_w, box_h, GxEPD_WHITE);
  }
  while (display.nextPage());
  display.setRotation(1);
  display.setPartialWindow(box_x, box_y, box_w, box_h);
  
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, LOW);
  digitalWrite(13, HIGH);
  delay(1000);
  senzoryDS.requestTemperatures();
  delay(1000);
  float temperature = senzoryDS.getTempCByIndex(0);

  display.firstPage();
  do
  {
    display.fillRect(box_x, box_y, box_w, box_h, GxEPD_WHITE);
    display.setCursor(box_x, cursor_y);
    display.print(temperature, 1);
  }
  while (display.nextPage());
  delay(500);
  display.hibernate();

  Serial.begin(115200);
  while (!Serial && millis() < 5000);

  Serial.print(F("Connecting to SSID: "));
  Serial.println(ssid);
  status = WiFi.begin(ssid, pass);
  delay(500);

  while (status != WL_CONNECTED)
  {
    delay(500);
    status = WiFi.status();
  }

  printWifiStatus();
  Serial.print("Connecting to host ");
  Serial.println(MQTT_SERVER);

  while (!client.connect(MQTT_SERVER, MQTT_PORT))
  {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nConnected!");
  mqttClient.begin(client);
  Serial.print("Connecting to mqtt broker...");
  while (!mqttClient.connect("arduino", "public", "public"))
  {
    Serial.print(".");
    delay(1000);
  }
  Serial.println(" connected!");
  
  char msg[1024];
  snprintf(msg, 1024, "{\"temperature\": %.1f }", temperature);

  mqttClient.publish("bojler/temperature", msg);
  mqttClient.update();
  Serial.println("published!");
  mqttClient.update();
  delay(1000);
  mqttClient.disconnect();
  delay(1000);
  client.flush();
  delay(1000);
  client.stop();
  WiFi.disconnect(true, true);
  WiFi.mode(WIFI_OFF);
  delay(1000);
  Serial.println("disconected!");
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  digitalWrite(14, LOW);
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  esp_deep_sleep_start();
}




void loop() {

}
