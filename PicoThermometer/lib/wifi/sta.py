import network
from nonvolatile import Settings


STA = network.WLAN(network.STA_IF)
STA.active(True)
STA.config(pm=0xa11140)  # Diable powersave mode
if Settings["WiFi-passw"]:
    STA.connect(Settings["WiFi-SSID"], Settings["WiFi-passw"])
else:
    STA.config(security=0)
    STA.connect(Settings["WiFi-SSID"])


# def wait_for_wifi_connection():
#     max_s_wait = 5
#     while STA.status() != network.STAT_GOT_IP:
#         sleep_ms(1000)
#         if max_s_wait < 0:
#             print('wifi connection failed')
#             return False
#         max_s_wait -= 1
#     else:
#         print('connected')
#         status = STA.ifconfig()
#         print('ip = ' + status[0])
#         print(STA.status("rssi"))
#         return STA.status("rssi")


# def disconnect():
#     try:
#         MQTT.disconnect()
#         STA.disconnect()
#         return True
#     except Exception as e:
#         print(e)
#         return False
