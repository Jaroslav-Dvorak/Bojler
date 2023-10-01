from utime import sleep_ms
from gpio_definitions import BTN_1, BTN_2, BTN_3, GREEN_LED, DONE_PIN
from nonvolatile import Settings, settings_save, settings_load
from measurement import Bat_voltage
from lib.display import screens


if __name__ == '__main__':
    GREEN_LED.value(1)
    if Bat_voltage < 2.8:
        DONE_PIN.value(1)
    settings_load()

    device_run = True
    full_refresh = False
    if not BTN_1.value():
        import modes.mode_setup
    elif not BTN_2.value():
        from modes.mode_testing import wifi_test_and_pub_discovery
        device_run = wifi_test_and_pub_discovery()
        GREEN_LED.value(0)
        sleep_ms(10_000)
        screens.widgets.clear()
        screens.eink.show(screens.widgets.img, partial=False)
        sleep_ms(1000)
        screens.eink.deep_sleep()
        DONE_PIN.value(1)
        sleep_ms(1000)
    elif not BTN_3.value():
        Settings["widget"] += 1
        if Settings["widget"] > 1:
            Settings["widget"] = 0
        settings_save()
        sleep_ms(1000)
        full_refresh = True

    if device_run:
        from modes.mode_regular import measuring_onboard_temperature
        measuring_onboard_temperature(full_refresh)
