from time import sleep
import network
from lib.umqtt_simple import MQTTClient
from gpio_definitions import LED

ssid = "dvorak"
password = "Hlavni115"

broker = "192.168.151.201"
client_id = "bojler1"
mqtt_user = "mqtt"
mqtt_pass = "mqtt"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0xa11140)  # Diable powersave mode
wlan.connect(ssid, password)

mqtt = MQTTClient(client_id=client_id,
                  server=broker,
                  port=1883,
                  user=mqtt_user,
                  password=mqtt_pass,
                  keepalive=7200,
                  ssl=False
                  )


def wait_for_wifi_connection():
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            return True
        max_wait -= 1
        LED.on()
        print('waiting for connection...')
        sleep(0.5)
        LED.off()
        return False


def check_wifi_connection():
    # Handle connection error
    if wlan.status() != 3:
        print('wifi connection failed')
        return False
    else:
        print('connected')
        LED.on()
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        return True


def connect_mqtt():
    try:
        mqtt.connect()
        return True
    except Exception as e:
        wlan.disconnect()
        print(e)
        return False


def publish(topic, value):
    print(topic)
    print(value)
    try:
        mqtt.publish(topic, value)
        print("publish Done")
        return True
        # publish("Bojler", '{"jimka": ' + disp_msg + ', "ambient": ' + onboard_temperature + '}')
    except Exception as e:
        print(e)
        wlan.disconnect()
        return False


def disconnect():
    try:
        mqtt.disconnect()
        wlan.disconnect()
        LED.off()
        return True
    except Exception as e:
        print(e)
        return False