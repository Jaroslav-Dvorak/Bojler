from utime import sleep_ms, time
from lib.display import screens
from gpio_definitions import DONE_PIN
from lib.wifi.ha import MQTT, send_discovery

from nonvolatile import Settings
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

ECONCLOSE = 1   # Connection closed by host
EREADLEN = 2    # Wrong length of read data
EWRITELEN = 3   # Wrong length of write data
ESTRTOLONG = 4  # String too long !!!!
ERESPONSE = 6   # Wrong response
EKEEPALIVE = 7  # Connection keep time has been exceeded (umqtt.robust2)
ENOCON = 8      # No connection

ECONUNKNOWN = 20     # Connection refused, unknown error
ECONPROTOCOL = 21    # Connection refused, unacteptable protocol version
ECONREJECT = 22      # Connection refused, identifier rejected
ECONUNAVAIBLE = 23   # Connection refused, server unavaible
ECONCREDENTIALS = 24 # Connection refused, bad credentials
ECONAUTH = 25        # Connection refused, not authorized
ECONNOT = 28         # No connection
ECONLENGTH = 29      # Connection, control packet type, Remaining Length != 2
ECONTIMEOUT = 30     # Connection timeout

ESUBACKUNKNOWN = 40  # Subscribe confirm unknown fail, SUBACK
ESUBACKFAIL = 44     # Subscribe confirm response: Failure

# Status code numbers from set_callback_status()
STIMEOUT = 0    # timeout
SDELIVERED = 1  # successfully delivered
SUNKNOWNPID = 2 # Unknown PID. It is also possible that the PID is outdated,
                # i.e. it came out of the message timeout.


def text_row(text, row):
    row = (row-1)*10
    screens.widgets.tiny_text(text, 0, row)
    screens.eink.show(screens.widgets.img, partial=True)


def erase_row(row):
    y = (row - 1) * 10
    h = 8
    screens.widgets.fill_rect(x=0, y=y, w=screens.eink.height, h=h, color=1)


def wifi_test_and_pub_discovery():
    screens.widgets.clear()
    screens.eink.show(screens.widgets.img, partial=False)
    ssid = Settings["WiFi-SSID"]
    mqtt = Settings["MQTT-brokr"]
    if not ssid:
        text_row("WiFi is not set.", 1)
        text_row("Device is turning off.", 2)
        return
    if not mqtt:
        text_row("MQTT is not set.", 1)
        text_row("Device is turning off.", 2)
        return

    from lib.wifi.sta import STA

    text_row(f"Connecting to '{ssid}'.", 1)
    start_time = time()
    try_time_s = 10
    while STA.status() != network.STAT_GOT_IP:
        erase_row(2)
        status = WIFI_STATUS.get(STA.status(), "UNKNOWN STATUS")
        text_row(status, 2)
        sleep_ms(10)
        if time() > start_time+try_time_s:
            text_row("Wifi connection failed,", 3)
            text_row("Device is turning off.", 4)
            return
    else:
        erase_row(2)
        status = WIFI_STATUS.get(STA.status(), "UNKNOWN STATUS")
        text_row(status, 2)
        rssi = STA.status("rssi")
        text_row(f"WiFi connected, rssi:{rssi}dBm", 3)

    sleep_ms(200)

    text_row(f"MQTT connecting {mqtt}", 4)
    try:
        MQTT.connect()
        text_row("MQTT connected", 5)
    except Exception as e:
        STA.disconnect()
        text_row(str(e), 5)
        text_row("Device is turning off.", 6)
        sleep_ms(1000)
        return

    sleep_ms(200)

    try:
        send_discovery(name="temperature", unit="C", device_class="temperature")
        send_discovery(name="soc", unit="%", device_class="battery")
        send_discovery(name="signal", unit="dBm", device_class="signal_strength")
        text_row("MQTT HA discovery published", 6)
    except Exception as e:
        STA.disconnect()
        e = int(str(e))
        e = MQTT_ERRS.get(e, "UNKNOWN ERROR")
        text_row(e, 6)
        text_row("Device is turning off.", 7)
        sleep_ms(1000)
        return

    text_row("Everything OK.", 7)
    MQTT.disconnect()
    sleep_ms(100)
    STA.disconnect()
    sleep_ms(1000)
    text_row("Device is turning off.", 8)
