import json
import machine
from lib.wifi.umqtt_simple import MQTTClient
from nonvolatile import Settings

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


def send_discovery(name, unit, device_class):
    topic = f"{DISCOVERY_PREFIX}/sensor/{DEVICE_NAME}/{name}/config".encode("utf-8")
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
    msg = msg.encode(msg, "utf-8")
    MQTT.publish(topic, msg, retain=True, qos=1)


def send_state(**kwargs):
    try:
        topic = f"{DEVICE_NAME}/sensor"
        payload = kwargs
        msg = json.dumps(payload)
        MQTT.publish(topic, msg, retain=False, qos=1)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def connect_mqtt():
    try:
        MQTT.connect()
        return True
    except Exception as e:
        print(e)
        return False


def disconnect_mqtt():
    try:
        MQTT.disconnect()
        return True
    except Exception as e:
        print(e)
        return False
