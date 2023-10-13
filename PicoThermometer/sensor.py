
# _____________________DS18X20_____________________________________________________


# _____________________SCD4X_____________________________________________________

# from machine import I2C, Pin
# from sensors.scd4x import SCD4X
#
# I2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400_000)
# sensor = SCD4X(I2c)

# _______________________SOIL MOISTURE_________________________________________)

from machine import ADC
from sensors.soil_moisture import SoilMoisture

adc = ADC(26)
sensor = SoilMoisture(adc)
