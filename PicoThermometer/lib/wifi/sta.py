from utime import sleep_ms
import machine
import network
from lib.wifi.umqtt_simple import MQTTClient
from nonvolatile import Settings


STA = network.WLAN(network.STA_IF)
STA.active(True)
STA.config(pm=0xa11140)  # Diable powersave mode
if Settings["WiFi-passw"]:
    STA.connect(Settings["WiFi-SSID"], Settings["WiFi-passw"])
else:
    STA.config(security=0)
    STA.connect(Settings["WiFi-SSID"])


MQTT = MQTTClient(client_id=machine.unique_id().hex(),
                  server=Settings["MQTT-brokr"],
                  port=1883,
                  user=Settings["MQTT-user"],
                  password=Settings["MQTT-passw"],
                  keepalive=7200,
                  ssl=False
                  )


def wait_for_wifi_connection():
    max_s_wait = 5
    while STA.status() != network.STAT_GOT_IP:
        sleep_ms(1000)
        if max_s_wait < 0:
            print('wifi connection failed')
            return False
        max_s_wait -= 1
    else:
        print('connected')
        status = STA.ifconfig()
        print('ip = ' + status[0])
        print(STA.status("rssi"))
        return STA.status("rssi")


def connect_mqtt():
    try:
        MQTT.connect()
        return True
    except Exception as e:
        STA.disconnect()
        print(e)
        return False


def publish(topic, msg):
    print("topic:", topic, "msg:", msg)
    try:
        MQTT.publish(topic, msg, qos=1)
        print("publish Done")
        return True
    except Exception as e:
        print(e)
        MQTT.disconnect()
        return False


def disconnect():
    try:
        MQTT.disconnect()
        STA.disconnect()
        return True
    except Exception as e:
        print(e)
        return False
