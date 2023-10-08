import lib.display.screens as screens
from gpio_definitions import TEMPER_ADC
import measurement
from helpers import voltage_to_soc, num_to_byte, byte_to_num
from nonvolatile import Settings, save_value, get_last_values


def measuring_onboard_temperature(full_refresh, minimum=15, maximum=35):
    bat_soc = voltage_to_soc(measurement.Bat_voltage)

    temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
    onboard_temperature = (27 - (temper_onboard_voltage - 0.706) / 0.001721)
    onboard_temperature = round(onboard_temperature, 1)

    filesize, byte_values = get_last_values(249, "temperatures.dat")

    values = [byte_to_num(value, minimum, maximum) for value in byte_values]
    values.append(onboard_temperature)

    if full_refresh or filesize % 50 == 0:
        full_refresh = True

    if Settings["widget"] == 0:
        screens.show_chart(values, minimum, maximum, bat_soc, full_refresh)
    elif Settings["widget"] == 1:
        screens.show_big_val(onboard_temperature, bat_soc, full_refresh)

    one_byte_value = num_to_byte(onboard_temperature, minimum, maximum)
    save_value(one_byte_value, "temperatures.dat")

    return onboard_temperature, bat_soc
