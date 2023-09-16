import machine
import os
from time import sleep
import lib.display.screens as screens
import measurement
from gpio_definitions import DONE_PIN, TEMPER_ADC, BATT_ADC, BTN_1, GREEN_LED
from helpers import voltage_to_soc
from lib.wifi.ap import start_ap, start_web

black = 0
white = 1

if __name__ == '__main__':
    bat_voltage = measurement.measure_analog(BATT_ADC)
    bat_voltage = round(bat_voltage * 2, 2)
    bat_soc = voltage_to_soc(bat_voltage)

    if not BTN_1.value():
        ip = start_ap("MYWIFITST")
        screens.show_overview(bat_voltage, ip)
        sleep(1)
        BTN_1.irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda x: machine.reset())
        start_web()

    while True:
        # GREEN_LED.value(1)
        bat_voltage = measurement.measure_analog(BATT_ADC)
        bat_voltage = round(bat_voltage * 2, 2)
        bat_soc = voltage_to_soc(bat_voltage)

        temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
        onboard_temperature = (27 - (temper_onboard_voltage - 0.706) / 0.001721)
        onboard_temperature = round(onboard_temperature, 1)

        screens.show_chart(onboard_temperature, bat_soc)
        # sleep(3)
        screens.show_big_val(onboard_temperature, bat_soc)
        # sleep(3)
        screens.show_qr_code('SPD*1.0*ACC:CZ2806000000000168540115*AM:450.00*CC:CZK*PT:IP*MSG:PLATBA ZA ZBOZI*X-VS:1234567890')

        GREEN_LED.value(0)

        DONE_PIN.value(1)
        sleep(1)
