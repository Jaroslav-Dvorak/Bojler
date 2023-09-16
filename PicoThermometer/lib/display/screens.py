import machine
import os
import gc
from lib.display.widgets import Widgets
from lib.display.epd_2in13_bw import Epd2in13bw
from gpio_definitions import BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI
import nonvolatile
from lib.display.drawing_bw import BLACK
from helpers import num_to_one_byte, one_byte_to_num, ONBOARD_TEMP_CONV_TO_BYTE


widgets = Widgets()
eink = Epd2in13bw(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI)


def show_chart(chart_val, batt_soc):
    filesize, values = nonvolatile.get_last_values(249, "temperatures.dat")
    one_byte_chart_val = num_to_one_byte(chart_val, *ONBOARD_TEMP_CONV_TO_BYTE)
    nonvolatile.save_value(one_byte_chart_val, "temperatures.dat")
    values = [one_byte_to_num(temp, *ONBOARD_TEMP_CONV_TO_BYTE) for temp in values]

    batt_coor = 150, 0
    values.append(chart_val)
    if len(values) > 250:
        values.pop(0)
    widgets.clear()
    widgets.chart(values, minimum=15, maximum=35)
    widgets.battery_indicator(batt_soc, *batt_coor)

    partial = not(filesize % nonvolatile.Settings["full_refresh_cadence"] == 0)
    eink.show(widgets.img, partial=partial)


def show_big_val(value, battery_soc):
    one_byte_chart_val = num_to_one_byte(value, *ONBOARD_TEMP_CONV_TO_BYTE)
    nonvolatile.save_value(one_byte_chart_val, "temperatures.dat")

    value_coor = 5, 25
    batt_coor = 210, 0
    widgets.clear()
    widgets.large_text(str(value), *value_coor)
    widgets.battery_indicator(battery_soc, *batt_coor)
    eink.show(widgets.img, partial=True)


def show_overview(batt_voltage, ip):
    widgets.clear()
    s = os.statvfs('/')
    memory_alloc = f"RAM alloc:      {gc.mem_alloc()//1024} kB "
    memory_free =  f"RAM free:       {gc.mem_free()//1024} kB"
    storage =      f"Free storage:   {s[0] * s[3] // 1024} kB"
    cpu =          f"CPU Freq:       {machine.freq() // 1000000} Mhz"
    batt_voltage = f"Batt voltage:   {batt_voltage} V"
    ip =           f"IP:             {ip}"

    widgets.tiny_text(memory_alloc, 0, 0)
    widgets.tiny_text(memory_free, 0, 10)
    widgets.tiny_text(storage, 0, 20)
    widgets.tiny_text(cpu, 0, 30)
    widgets.tiny_text(batt_voltage, 0, 40)
    widgets.tiny_text(ip, 0, 50)
    eink.show(widgets.img, partial=False)
