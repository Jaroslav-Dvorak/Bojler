from machine import reset
from time import sleep
from eink import show, Eink
import wireless
import measurement
from gpio_definitions import *
import json


if __name__ == '__main__':
    # bat_max_voltage = 4.0
    # bat_min_voltage = 2.5
    #
    # full_scale = bat_max_voltage - bat_min_voltage  # 1.5
    # curr_on_scale = bat_max_voltage - bat_voltage   # 0.3

    eink = Eink()
    eink.clear()

    bat_voltage = measurement.measure_analog(BATT_ADC) * 2
    soc = int((1 - ((4.0 - bat_voltage)/1.5)) * 100)
    soc = 0 if soc < 0 else soc

    temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
    onboard_temperature = 27 - (temper_onboard_voltage - 0.706) / 0.001721

    rom_1 = bytearray(b'(\t)\x93 "\t\xb2')
    rom_2 = bytearray(b'(\xf8\xe4\x13\x0f\x00\x00\xe7')
    rom_3 = bytearray(b'(r\x81\x80\xe3\xe1=\xe6')

    onewire1 = measurement.MeasureOnewire(TEMP_SENS_1, rom_1)
    onewire2 = measurement.MeasureOnewire(TEMP_SENS_2, rom_2)
    onewire3 = measurement.MeasureOnewire(TEMP_SENS_3, rom_3)
    onewire1.convert()
    onewire2.convert()
    onewire3.convert()

    sleep(0.75)

    temperature_1 = onewire1.get_temp()
    temperature_2 = onewire2.get_temp()
    temperature_3 = onewire3.get_temp()

    # temperature_1 = measurement.measure_onewire(TEMP_SENS_1)
    # temperature_2 = measurement.measure_onewire(TEMP_SENS_2)
    # temperature_3 = measurement.measure_onewire(TEMP_SENS_3)

    eink.show(onboard_temperature, temperature_1, temperature_2, temperature_3, soc)

    if wireless.wait_for_wifi_connection():
        if wireless.check_wifi_connection():
            if wireless.connect_mqtt():
                temperature_1 = int(temperature_1*10) if temperature_1 is not None else None
                temperature_2 = int(temperature_2*10) if temperature_2 is not None else None
                temperature_3 = int(temperature_3*10) if temperature_3 is not None else None
                mqtt_msg = {"ambient": int(onboard_temperature*10), "output": temperature_1, "gauge": temperature_2, "sump": temperature_3, "soc": soc}
                mqtt_msg = json.dumps(mqtt_msg)
                wireless.publish("Bojler", mqtt_msg)

    wireless.disconnect()
    sleep(1)
    DONE_PIN.value(1)
    sleep(1)
    reset()
