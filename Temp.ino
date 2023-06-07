
// base class GxEPD2_GFX can be used to pass references or pointers to the display instance as parameter, uses ~1.2k more code
// enable or disable GxEPD2_GFX base class
#define ENABLE_GxEPD2_GFX 0

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <Fonts/FreeMonoBold24pt7b.h>

#include <OneWire.h>
#include <DallasTemperature.h>

// ESP32 SS=5,SCL(SCK)=18,SDA(MOSI)=23,BUSY=15,RST=2,DC=0

// 2.13'' EPD Module
GxEPD2_BW<GxEPD2_213_BN, GxEPD2_213_BN::HEIGHT> display(GxEPD2_213_BN(/*CS=5*/ 5, /*DC=*/ 21, /*RST=*/ 2, /*BUSY=*/ 15)); // DEPG0213BN 122x250, SSD1680
//GxEPD2_3C<GxEPD2_213_Z98c, GxEPD2_213_Z98c::HEIGHT> display(GxEPD2_213_Z98c(/*CS=5*/ 5, /*DC=*/ 0, /*RST=*/ 2, /*BUSY=*/ 15)); // GDEY0213Z98 122x250, SSD1680

// 2.9'' EPD Module
//GxEPD2_BW<GxEPD2_290_BS, GxEPD2_290_BS::HEIGHT> display(GxEPD2_290_BS(/*CS=5*/ 5, /*DC=*/ 0, /*RST=*/ 2, /*BUSY=*/ 15)); // DEPG0290BS 128x296, SSD1680
//GxEPD2_3C<GxEPD2_290_C90c, GxEPD2_290_C90c::HEIGHT> display(GxEPD2_290_C90c(/*CS=5*/ 5, /*DC=*/ 21, /*RST=*/ 2, /*BUSY=*/ 15)); // GDEM029C90 128x296, SSD1680

const int pinCidlaDS = 14;
OneWire oneWireDS(pinCidlaDS);
DallasTemperature senzoryDS(&oneWireDS);

void setup()
{
  display.init(115200, true, 50, false);
  delay(1000);
  if (display.epd2.hasFastPartialUpdate)
  {
    showPartialUpdate();
    delay(1000);
  }
  display.hibernate();
}

void showPartialUpdate()
{
  uint16_t box_x = 10;
  uint16_t box_y = 10;
  uint16_t box_w = 230;
  uint16_t box_h = 102;
  uint16_t cursor_y = box_y + box_h - 30;
  if (display.epd2.WIDTH < 104) cursor_y = box_y + 6;
  float value = 13.95;
  uint16_t incr = display.epd2.hasFastPartialUpdate ? 1 : 3;
  display.setFont(&FreeMonoBold24pt7b);
  display.setTextSize(2);
  if (display.epd2.WIDTH < 104) display.setFont(0);
  display.setTextColor(GxEPD_BLACK);
  // show where the update box is

  display.firstPage();
  do
  {
    display.fillRect(box_x, box_y, box_w, box_h, GxEPD_WHITE);
  }
  while (display.nextPage());
  delay(1000);


  // show updates in the update box
    display.setRotation(1);
    display.setPartialWindow(box_x, box_y, box_w, box_h);
    for (uint16_t i = 1; i <= 1000; i += incr)
    {

      senzoryDS.requestTemperatures();

      display.firstPage();
      do
      {
        display.fillRect(box_x, box_y, box_w, box_h, GxEPD_WHITE);
        display.setCursor(box_x, cursor_y);
        display.print(senzoryDS.getTempCByIndex(0), 1);
      }
      while (display.nextPage());
      delay(500);
    }
}

void loop() {
  // put your main code here, to run repeatedly:
}
