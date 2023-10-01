from utime import sleep_ms, time
from lib.display import screens
from gpio_definitions import DONE_PIN

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

discovery_msg = "discoverymsg"
discovery_tpc = "thedisctopic"


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

    from lib.wifi import sta

    text_row(f"Connecting to '{ssid}'.", 1)
    start_time = time()
    try_time_s = 10
    while sta.STA.status() != network.STAT_GOT_IP:
        erase_row(2)
        status = WIFI_STATUS.get(sta.STA.status(), "UNKNOWN STATUS")
        text_row(status, 2)
        sleep_ms(10)
        if time() > start_time+try_time_s:
            text_row("Wifi connection failed,", 3)
            text_row("Device is turning off.", 4)
            return
    else:
        erase_row(2)
        status = WIFI_STATUS.get(sta.STA.status(), "UNKNOWN STATUS")
        text_row(status, 2)
        text_row("WiFi connected.", 3)

    sleep_ms(200)

    text_row(f"MQTT connecting {mqtt}", 4)
    try:
        sta.MQTT.connect()
        text_row("MQTT connected", 5)
    except Exception as e:
        sta.STA.disconnect()
        text_row(str(e), 5)
        text_row("Device is turning off.", 6)
        sleep_ms(1000)
        return

    sleep_ms(200)

    try:
        sta.MQTT.publish(discovery_tpc, discovery_msg, qos=1)
        text_row("MQTT HA discovery published", 6)
    except Exception as e:
        sta.STA.disconnect()
        text_row(e, 5)
        sleep_ms(1000)
        return

    text_row("Everything OK.", 7)
    text_row("Device is turning off.", 8)
    sta.STA.disconnect()
    sleep_ms(1000)


# screens.show_qr_code(
#             'SPD*1.0*ACC:CZ2806000000000168540115*AM:450.00*CC:CZK*PT:IP*MSG:PLATBA ZA ZBOZI*X-VS:1234567890', 0, 0, 3
# )
#

# DONE_PIN.value(1)
