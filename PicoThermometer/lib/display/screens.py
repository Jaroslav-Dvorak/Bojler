from lib.display.widgets import Widgets
from lib.display.epd_2in13_bw import Epd2in13bw
from gpio_definitions import BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI
import nonvolatile
from drawing_bw import BLACK
from helpers import num_to_one_byte, one_byte_to_num, ONBOARD_TEMP_CONV_TO_BYTE


widgets = Widgets()
eink = Epd2in13bw(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI)


def show_chart(chart_val, batt_val):
    filesize, values = nonvolatile.get_last_values(249, "temperatures.dat")
    one_byte_chart_val = num_to_one_byte(chart_val, *ONBOARD_TEMP_CONV_TO_BYTE)
    nonvolatile.save_value(one_byte_chart_val, "temperatures.dat")
    values = [one_byte_to_num(temp, *ONBOARD_TEMP_CONV_TO_BYTE) for temp in values]

    widgets.chart(values, minimum=15, maximum=35)
    eink.load_previous(widgets.img)

    values.append(chart_val)
    if len(values) > 250:
        values.pop(0)
    widgets.clear()
    widgets.chart(values, minimum=15, maximum=35)

    bat_voltage = str(batt_val) + "V"
    widgets.tiny_text(bat_voltage, 60, 0, BLACK)

    if filesize % nonvolatile.Settings["full_refresh_cadence"] == 0:
        eink.show_full(widgets.img)
    else:
        eink.show_partial(widgets.img)


def show_big_val(value):
    filesize, previous_value = nonvolatile.get_last_values(1, "temperatures.dat")
    one_byte_chart_val = num_to_one_byte(value, *ONBOARD_TEMP_CONV_TO_BYTE)
    nonvolatile.save_value(one_byte_chart_val, "temperatures.dat")
    previous_value = one_byte_to_num(previous_value[0], *ONBOARD_TEMP_CONV_TO_BYTE)

    x = 5
    y = 25
    widgets.large_text(str(previous_value), x, y)
    eink.load_previous(widgets.img)
    widgets.clear()
    widgets.large_text(str(value), x, y)

    # bat_voltage = str(batt_val) + "V"
    # widgets.tiny_text(bat_voltage, 60, 0, BLACK)

    if filesize % nonvolatile.Settings["full_refresh_cadence"] == 0:
        eink.show_full(widgets.img)
    else:
        eink.show_partial(widgets.img)
