from machine import Pin, ADC

# display WeAct
# 1 Busy    purple
# 2 Res     orange
# 3 D/C     white
# 4 CS      blue
# 5 SCL     green
# 6 SDA     yellow
# 7 GND     black
# 8 VCC     red
vcc_pin = Pin(5, Pin.OUT).value(1)
BUSY_PIN = Pin(8, Pin.IN, Pin.PULL_UP)
RST_PIN = Pin(7, Pin.OUT)
DC_PIN = Pin(6, Pin.OUT)
CS_PIN = Pin(4, Pin.OUT)
SDA_PIN = Pin(3)  # SDA=MOSI
SCL_PIN = Pin(2)  # SCL=SCK
SPI_NUM = 0

# tp5110
DONE_PIN = Pin(22, Pin.OUT)

# analog
BATT_ADC = ADC(28)
TEMPER_ADC = ADC(4)

# dallas
# TEMP_SENS_1 = Pin(0)
# TEMP_SENS_2 = Pin(1)
# TEMP_SENS_3 = Pin(2)

# led
LED = Pin('LED', Pin.OUT)
