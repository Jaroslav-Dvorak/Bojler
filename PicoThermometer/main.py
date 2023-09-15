# from machine import reset
from time import sleep
# from eink import Eink
# import wireless
from lib.display.epd_2in13_bw import Epd2in13bw
from lib.display.widgets import Widgets
import measurement
from gpio_definitions import *
# import micropython
import os
import gc
import machine
import nonvolatile
from random import randint
# import json

black = 0
white = 1

eink = Epd2in13bw(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI)
widgets = Widgets()

temperatures = nonvolatile.get_last_values(249, "temperatures.dat")
temperatures = [temp / 10 + 25 for temp in temperatures]
widgets.chart(temperatures, minimum=15, maximum=35)
eink.load_previous(widgets.img)


if __name__ == '__main__':
    while True:
        s = os.statvfs('/')
        memory = f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used."
        storage = f"Free storage: {s[0] * s[3] / 1024} KB"
        cpu = f"CPU Freq: {machine.freq()/1000000}Mhz"

        temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
        onboard_temperature = 27 - (temper_onboard_voltage - 0.706) / 0.001721
        optimized_temp = int((onboard_temperature-25)*10)
        if optimized_temp < -127:
            optimized_temp = -127
        elif optimized_temp > 128:
            optimized_temp = 128

        bat_voltage = round(measurement.measure_analog(BATT_ADC) * 2, 2)
        bat_voltage = str(round(bat_voltage, 2)) + "V"
        widgets.tiny_text(bat_voltage, 60, 0, black)

        temperatures.append(onboard_temperature)
        temperatures.pop(0)
        widgets.clear()
        widgets.chart(temperatures, minimum=15, maximum=35)
        nonvolatile.save_value(optimized_temp, "temperatures.dat")

        eink.show_partial(widgets.img)
        sleep(1)
        DONE_PIN.value(1)
        sleep(1)
        widgets.clear()
