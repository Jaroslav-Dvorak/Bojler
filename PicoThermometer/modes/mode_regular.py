import lib.display.screens as screens
import measurement
from nonvolatile import Settings, save_value, get_last_values, num_to_byte, byte_to_num


def load_show_save(full_refresh, bat_soc, minimum=15, maximum=35):
    minimum = 0
    maximum = 80

    # value = measurement.onboard_temperature()
    value = measurement.measure_dallas()

    filesize, byte_values = get_last_values(249, "temperatures.dat")

    values = [byte_to_num(val, minimum, maximum) for val in byte_values]
    values.append(value)

    if full_refresh or filesize % 50 == 0:
        full_refresh = True

    if Settings["widget"] == 0:
        screens.show_chart(values, minimum, maximum, bat_soc, full_refresh)
    elif Settings["widget"] == 1:
        screens.show_big_val(value, bat_soc, full_refresh)

    one_byte_value = num_to_byte(value, minimum, maximum)
    save_value(one_byte_value, "temperatures.dat")

    return value
