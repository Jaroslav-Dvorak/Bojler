from machine import Pin, ADC
from machine import SPI as Spi

# display WeAct
# 1 Busy    purple
# 2 Res     orange
# 3 D/C     white
# 4 CS      blue
# 5 SCL     green
# 6 SDA     yellow
# 7 GND     black
# 8 VCC     red
BUSY_PIN = Pin(10, Pin.IN, Pin.PULL_UP)
RST_PIN = Pin(11, Pin.OUT)
DC_PIN = Pin(12, Pin.OUT)
CS_PIN = Pin(13, Pin.OUT)
SCL_PIN = Pin(14)  # SCL=SCK
SDA_PIN = Pin(15)  # SDA=MOSI
SPI_NUM = 1
SPI = Spi(SPI_NUM, baudrate=1_000_000, sck=SCL_PIN, mosi=SDA_PIN)

# tp5110
DONE_PIN = Pin(0, Pin.OUT)

# analog
BATT_ADC = ADC(28)
TEMPER_ADC = ADC(4)

# dallas
# TEMP_SENS_1 = Pin(0)
# TEMP_SENS_2 = Pin(1)
# TEMP_SENS_3 = Pin(2)

# led
LED = Pin('LED', Pin.OUT)
