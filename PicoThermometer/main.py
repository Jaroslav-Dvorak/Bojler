from lib.wifi.sta import STA, wait_for_wifi_connection, wifi_connect
wifi_active = wifi_connect()

from nonvolatile import Settings, settings_save, settings_load
from utime import sleep_ms
from gpio_definitions import BTN_1, BTN_2, BTN_3, GREEN_LED, DONE_PIN
from measurement import Bat_voltage
from lib.display import screens


if __name__ == '__main__':
    if Bat_voltage < 2.8:
        DONE_PIN.value(1)
    settings_load()

    device_run = True
    full_refresh = False
    if not BTN_1.value():
        from modes.mode_setup import start_setup
        start_setup("HBD_SETUP")

    elif not BTN_2.value():
        import modes.mode_testing as testing
        screens.clear_display()
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
        from modes.mode_regular import measuring_onboard_temperature
        while True:
            onboard_temperature, bat_soc = measuring_onboard_temperature(full_refresh)

            rssi = None
            if wifi_active:
                rssi = wait_for_wifi_connection()
                if rssi:
                    from lib.wifi.ha import send_state, connect_mqtt
                    if connect_mqtt():
                        sleep_ms(200)
                        GREEN_LED.value(1)
                        send_state(temperature=onboard_temperature,
                                   soc=bat_soc,
                                   signal=rssi)
                STA.disconnect()

                screens.widgets.signal_indicator(rssi, 40, 10)
                screens.eink.show(screens.widgets.img, partial=True)

            GREEN_LED.value(0)
            screens.eink.deep_sleep()
            sleep_ms(100)
            DONE_PIN.value(1)
            sleep_ms(10_000)

            full_refresh = False
