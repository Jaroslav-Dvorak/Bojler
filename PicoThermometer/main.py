# from machine import reset
from time import sleep
# from eink import Eink
# import wireless
from lib.display.epd_2in13_BW import Epd2in13bw
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

if __name__ == '__main__':
    i = 0
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

        # temperatures = nonvolatile.save_and_get_last_values(int(onboard_temperature), "temperatures.dat")
        temperatures = nonvolatile.save_and_get_last_values(optimized_temp, "temperatures.dat")

        temperatures = [temp/10+25 for temp in temperatures]
        # temperatures = nonvolatile.save_and_get_last_values(i, "temperatures.dat")
        i += 1
        # eink.show(str(round(onboard_temperature, 1)))

        widgets.chart(temperatures, minimum=15, maximum=35)
        # y = 0
        # for i in range(20):
        #     eink.eink.text(str(i), 150, y, black)
        #     # eink.eink.rect(150-1, y-1, 10, 11, black)
        #     eink.eink.hline(150, y+8, 8, black)
        #     y += 10

        bat_voltage = measurement.measure_analog(BATT_ADC) * 2
        # soc = int((1 - ((4.0 - bat_voltage)/1.5)) * 100)
        # soc = 0 if soc < 0 else soc
        bat_voltage = str(round(bat_voltage, 2)) + "V"
        widgets.tiny_text(bat_voltage, 60, 0, black)

        eink.show(widgets.buffer_black)
        # eink.eink.display(eink.eink.buffer)
        # eink.eink.display_Partial(eink.eink.buffer)

        # y = 0
        #
        # for _ in range(20):
        #     eink.eink.hline(150, y+8, 8, white)
        #     eink.eink.display_Partial(eink.eink.buffer)
        #     eink.eink.hline(150, y + 8, 8, black)
        #     eink.eink.display_Partial(eink.eink.buffer)

        # gc.collect()

        # machine.lightsleep(60000)
        # break
        sleep(1)
        DONE_PIN.value(1)
        sleep(10)
        widgets.canvas_black.fill(1)
