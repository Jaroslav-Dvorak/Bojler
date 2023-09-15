import machine
import os
from time import sleep
import gc
from lib.display.screens import show_chart, show_big_val
import measurement
from gpio_definitions import DONE_PIN, TEMPER_ADC, BATT_ADC

black = 0
white = 1

if __name__ == '__main__':

    while True:
        s = os.statvfs('/')
        memory = f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used."
        storage = f"Free storage: {s[0] * s[3] / 1024} KB"
        cpu = f"CPU Freq: {machine.freq()/1000000}Mhz"

        temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
        onboard_temperature = (27 - (temper_onboard_voltage - 0.706) / 0.001721)
        onboard_temperature = round(onboard_temperature, 1)
        # bat_voltage = measurement.measure_analog(BATT_ADC)
        # bat_voltage = round(bat_voltage * 2, 2)

        # show_chart(onboard_temperature, bat_voltage)
        show_big_val(onboard_temperature)

        sleep(1)
        DONE_PIN.value(1)
        sleep(1)
