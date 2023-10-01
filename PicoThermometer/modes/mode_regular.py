from utime import sleep_ms
import lib.display.screens as screens
from gpio_definitions import DONE_PIN, TEMPER_ADC, GREEN_LED
import measurement
from helpers import voltage_to_soc
from nonvolatile import Settings


def measuring_onboard_temperature(full_refresh):

    while True:
        bat_soc = voltage_to_soc(measurement.Bat_voltage)

        temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
        onboard_temperature = (27 - (temper_onboard_voltage - 0.706) / 0.001721)
        onboard_temperature = round(onboard_temperature, 1)

        if Settings["widget"] == 0:
            screens.show_chart(onboard_temperature, bat_soc, full_refresh)
        elif Settings["widget"] == 1:
            screens.show_big_val(onboard_temperature, bat_soc, full_refresh)

        GREEN_LED.value(0)
        screens.eink.deep_sleep()
        sleep_ms(100)
        DONE_PIN.value(1)
        sleep_ms(10_000)

        full_refresh = False
