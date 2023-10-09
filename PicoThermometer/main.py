from nonvolatile import Settings, settings_save, settings_load
settings_load()
from lib.wifi.sta import STA, wait_for_wifi_connection, wifi_connect
wifi_active = wifi_connect()

from time import sleep_ms
from gpio_definitions import BTN_1, BTN_2, BTN_3, GREEN_LED, DONE_PIN
from measurement import batt_voltage, voltage_to_soc
from lib.display import screens


if __name__ == '__main__':
    battery_voltage = batt_voltage()
    if battery_voltage < 2.8:
        DONE_PIN.value(1)
    bat_soc = voltage_to_soc(battery_voltage)

    device_run = True
    full_refresh = False
    if not BTN_1.value():
        from modes.mode_setup import start_setup
        start_setup("HBD_SETUP", battery_voltage)

    elif not BTN_2.value():
        import modes.mode_testing as testing
        screens.clear_display()
        if testing.dallas_scan():
            if testing.check_settings():
                if testing.check_wifi():
                    sleep_ms(100)
                    if testing.check_mqtt():
                        sleep_ms(100)
                        if testing.try_ha_discovery():
                            testing.show_success()
        del testing
        while BTN_1.value() and BTN_2.value() and BTN_3.value():
            sleep_ms(100)
        full_refresh = True

    elif not BTN_3.value():
        Settings["widget"] += 1
        if Settings["widget"] > 1:
            Settings["widget"] = 0
        settings_save()
        sleep_ms(1000)
        full_refresh = True

    if device_run:
        mqtt_payload = {}
        from modes.mode_regular import load_show_save
        while True:
            value = load_show_save(full_refresh, bat_soc)
            mqtt_payload["soc"] = bat_soc
            rssi = None
            if wifi_active:
                rssi = wait_for_wifi_connection()
                if rssi:
                    from lib.wifi.ha import send_state, connect_mqtt, MQTT
                    if connect_mqtt():
                        GREEN_LED.value(1)
                        send_state(temperature=value,
                                   soc=bat_soc,
                                   signal=rssi)
                        MQTT.wait_msg()
                        MQTT.disconnect()
                        sleep_ms(500)
                STA.disconnect()
                sleep_ms(1000)
                # screens.widgets.rect()
                screens.widgets.signal_indicator(rssi, 40, 10)
                screens.eink.show(screens.widgets.img, partial=True)

            GREEN_LED.value(0)
            screens.eink.deep_sleep()
            sleep_ms(100)
            DONE_PIN.value(1)
            sleep_ms(10_000)

            full_refresh = False
            wifi_active = wifi_connect()
