from utime import sleep_ms
from collections import OrderedDict
import json
import machine
from lib.wifi.umqtt_simple import MQTTClient
from nonvolatile import Settings
import gc

BOARD_ID = machine.unique_id().hex()
DISCOVERY_PREFIX = "homeassistant"
DEVICE_NAME = Settings["MQTT-name"]

MQTT = MQTTClient(client_id=BOARD_ID,
                  server=Settings["MQTT-brokr"],
                  port=1883,
                  user=Settings["MQTT-user"],
                  password=Settings["MQTT-passw"],
                  keepalive=7200,
                  ssl=False
                  )

# device = OrderedDict([("identifiers", "[" + BOARD_ID + "]"),
#                       ("name", DEVICE_NAME),
#                       ("sw_version", "0.1.0"),
#                       ("model", "Machrovina_2"),
#                       ("manufacturer", "JardaDvorak")
#                       ])
# config = OrderedDict([
#     ("name", name),
#     ("state_topic", f"{DEVICE_NAME}/sensor"),
#     ("value_template", "{{ value_json." + name + " }}"),
#     ("unit_of_measurement", unit),
#     ("device", device),
#     ("force_update", False),
#     ("unique_id", name + BOARD_ID),
#     ("device_class", device_class)
# ])


def send_discovery(name, unit, device_class):
    topic = f"{DISCOVERY_PREFIX}/sensor/{DEVICE_NAME}/{name}/config"
    config = {
              "name": name,
              "state_topic": f"{DEVICE_NAME}/sensor",
              "value_template": "{{ value_json."+name+" }}",
              "unit_of_measurement": unit,
              "device": {"identifiers": BOARD_ID,
                         "name": DEVICE_NAME,
                         "sw_version": "0.1.0",
                         "model": "Machrovina_2",
                         "manufacturer": "JardaDvorak"
                         },
              "force_update": False,
              "unique_id": name+BOARD_ID,
              "device_class": device_class
              }
    msg = json.dumps(config)
    gc.collect()
    MQTT.publish(topic, msg, retain=True, qos=1)


def send_state(**kwargs):
    topic = f"{DEVICE_NAME}/sensor"
    payload = kwargs
    msg = json.dumps(payload)
    MQTT.publish(topic, msg, retain=False, qos=1)


def connect_mqtt():
    try:
        MQTT.connect()
        return True
    except Exception as e:
        # STA.disconnect()
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