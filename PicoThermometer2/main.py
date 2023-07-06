from machine import reset
from time import sleep
from eink import show
import wireless
import measurement
from gpio_definitions import *
import json


if __name__ == '__main__':
    batt_voltage = measurement.measure_analog(BATT_ADC) * 2
    soc = int(((1.5-(4.0 - batt_voltage)) / 1.5) * 100)

    temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
    onboard_temperature = int(27 - (temper_onboard_voltage - 0.706) / 0.001721)

    temperature_1 = measurement.measure_onewire(TEMP_SENS_1)
    temperature_2 = measurement.measure_onewire(TEMP_SENS_2)
    temperature_3 = measurement.measure_onewire(TEMP_SENS_3)

    show(onboard_temperature, temperature_1, temperature_2, temperature_3, soc)

    if wireless.wait_for_wifi_connection():
        if wireless.check_wifi_connection():
            if wireless.connect_mqtt():
                mqtt_msg = {"jimka": temperature_1, "rafika": temperature_2, "sroubeni": temperature_3}
                mqtt_msg = json.dumps(mqtt_msg)
                wireless.publish("Testjakpes", mqtt_msg)

    wireless.disconnect()
    sleep(1)
    DONE_PIN.value(1)
    sleep(1)
    reset()
