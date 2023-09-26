from utime import sleep
import machine
import lib.display.screens as screens
import measurement
from gpio_definitions import DONE_PIN, TEMPER_ADC, BATT_ADC, BTN_1, BTN_2, BTN_3, GREEN_LED
from helpers import voltage_to_soc
from lib.wifi.ap import start_ap, start_web
from nonvolatile import Settings, settings_save, settings_load

black = 0
white = 1

GREEN_LED.value(1)

if __name__ == '__main__':
    settings_load()
    bat_voltage = measurement.measure_analog(BATT_ADC)
    bat_voltage = round(bat_voltage * 2, 2)
    bat_soc = voltage_to_soc(bat_voltage)

    pref_widget = Settings["widget"]
    full_refresh = False
    if not BTN_1.value():
        ap_ssid = "MYWIFITST"
        ip = start_ap(ap_ssid)
        screens.show_overview(bat_voltage, ip, ap_ssid)
        start_web()
    elif not BTN_2.value():
        if pref_widget == 0:
            Settings["widget"] = 1
        elif pref_widget == 1:
            Settings["widget"] = 0
        settings_save()
        sleep(0.5)
        full_refresh = True
    elif not BTN_3.value():
        screens.show_qr_code(
            'SPD*1.0*ACC:CZ2806000000000168540115*AM:450.00*CC:CZK*PT:IP*MSG:PLATBA ZA ZBOZI*X-VS:1234567890', 0, 0, 3)
        DONE_PIN.value(1)

    while True:
        bat_voltage = measurement.measure_analog(BATT_ADC)
        bat_voltage = round(bat_voltage * 2, 2)
        bat_soc = voltage_to_soc(bat_voltage)

        temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
        onboard_temperature = (27 - (temper_onboard_voltage - 0.706) / 0.001721)
        onboard_temperature = round(onboard_temperature, 1)

        if Settings["widget"] == 0:
            screens.show_chart(onboard_temperature, bat_soc, full_refresh)
        elif Settings["widget"] == 1:
            screens.show_big_val(onboard_temperature, bat_soc, full_refresh)

        GREEN_LED.value(0)
        sleep(1)
        DONE_PIN.value(1)
        sleep(1)

        full_refresh = False
