# from machine import reset
# from time import sleep
from eink import Eink
# import wireless
import measurement
from gpio_definitions import *
# import json


if __name__ == '__main__':

    eink = Eink()
    eink.clear()

    temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
    onboard_temperature = 27 - (temper_onboard_voltage - 0.706) / 0.001721
    onboard_temperature = str(round(onboard_temperature, 1))

    # eink.show(onboard_temperature)
    eink.eink.fill(0xFF)
    eink.eink.line(-10, 0, 256, 130, 0x00)
    eink.eink.line(-10, 130, 256, 0, 0x00)
    # eink.eink.pixel(150, 200)
    eink.eink.display(eink.eink.buffer)
