from utime import sleep_ms, time
import network
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

        if Settings["WiFi-SSID"] and Settings["MQTT-brokr"]:
            from lib.wifi.sta import STA
            start_time = time()
            try_time_s = 10
            while STA.status() != network.STAT_GOT_IP:
                sleep_ms(10)
                if time() > start_time + try_time_s:
                    STA.disconnect()
                    break
            else:
                sleep_ms(200)
                from lib.wifi.ha import MQTT, send_state
                try:
                    MQTT.connect()
                except Exception as e:
                    STA.disconnect()
                else:
                    sleep_ms(200)
                    try:
                        send_state(temperature=onboard_temperature, soc=bat_soc, signal=STA.status("rssi"))
                    except Exception as e:
                        pass
                MQTT.disconnect()
                sleep_ms(200)
                STA.disconnect()

        GREEN_LED.value(0)
        screens.eink.deep_sleep()
        sleep_ms(100)
        DONE_PIN.value(1)
        sleep_ms(10_000)

        full_refresh = False
