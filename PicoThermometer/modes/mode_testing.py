from utime import sleep_ms, time
from lib.display.screens import text_row
from lib.wifi.ha import MQTT, send_discovery
from lib.wifi.sta import STA, wifi_connect
from sensor import get_serial

from nonvolatile import Settings, settings_save
import network


WIFI_STATUS = {
    network.STAT_IDLE: "IDLE",
    network.STAT_CONNECTING: "CONNECTING",
    network.STAT_WRONG_PASSWORD: "WRONG_PASSWORD",
    network.STAT_NO_AP_FOUND: "NO_AP_FOUND",
    network.STAT_CONNECT_FAIL: "CONNECT_FAIL",
    2: "OBTAINING_IP",
    network.STAT_GOT_IP: "GOT_IP"
}

MQTT_ERRS = {
    1: "ECONCLOSE",
    2: "EREADLEN",
    3: "EWRITELEN",
    4: "ESTRTOLONG",
    6: "ERESPONSE",
    7: "EKEEPALIVE",
    8: "ENOCON",

    20: "ECONUNKNOWN",
    21: "ECONPROTOCOL",
    22: "ECONREJECT",
    23: "ECONUNAVAIBLE",
    24: "ECONCREDENTIALS",
    25: "ECONAUTH",
    28: "ECONNOT",
    29: "ECONLENGTH",
    30: "ECONTIMEOUT",

    40: "ESUBACKUNKNOWN",
    41: "ESUBACKFAIL"
}

Continue_message = "Press any button..."


def sensor_scan():
    serial = get_serial()
    if serial:
        text_row(f"Sensor found: {serial}", 1)
        Settings["dallas_sens"] = serial
        settings_save()
        sleep_ms(1000)
        return True
    else:
        text_row("Sensor not found", 1)


def check_settings():
    ssid = Settings["WiFi-SSID"]
    mqtt = Settings["MQTT-brokr"]
    if not ssid:
        text_row("WiFi is not set.", 2)
        text_row(Continue_message, 3)
        return False
    if not mqtt:
        text_row("MQTT is not set.", 2)
        text_row(Continue_message, 3)
        return False
    return True


def check_wifi():
    wifi_connect()
    text_row(f"Connecting to {Settings['WiFi-SSID']}", 2)
    start_time = time()
    try_time_s = 10
    while STA.status() != network.STAT_GOT_IP:
        status = WIFI_STATUS.get(STA.status(), "UNKNOWN STATUS")
        text_row(status, 3)
        sleep_ms(10)
        if time() > start_time+try_time_s:
            text_row("Wifi connection failed,", 4)
            text_row(Continue_message, 5)
            STA.disconnect()
            return False
    else:
        status = WIFI_STATUS.get(STA.status(), "UNKNOWN STATUS")
        text_row(status, 3)
        rssi = STA.status("rssi")
        text_row(f"WiFi connected, rssi:{rssi}dBm", 4)
    return True


def check_mqtt():
    text_row(f"MQTT connecting {MQTT.server}", 5)
    try:
        MQTT.connect()
        text_row("MQTT connected", 6)
    except Exception as e:
        text_row(str(e), 6)
        text_row(Continue_message, 7)
        return False
    else:
        return True


def try_ha_discovery():
    try:
        send_discovery(name="temperature", unit="°C", device_class="temperature")
        send_discovery(name="soc", unit="%", device_class="battery")
        send_discovery(name="signal", unit="dBm", device_class="signal_strength")
        text_row("MQTT HA discovery published", 7)
    except Exception as e:
        e = int(str(e))
        e = MQTT_ERRS.get(e, "UNKNOWN ERROR")
        text_row(e, 7)
        text_row(Continue_message, 8)
        return False
    else:
        return True


def show_success():
    text_row("Everything OK :-)", 8)
    text_row(Continue_message, 9)
