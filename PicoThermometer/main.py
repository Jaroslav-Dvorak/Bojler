import machine

import framebuf
import time

from ds18x20 import read_temp_1sens
from epd_2in13 import EPD_2in13_V3_Landscape
from writer import Writer
import bigfont


import network
from umqtt_simple import MQTTClient


vcc_pin = machine.Pin(1, machine.Pin.OUT)
vcc_pin.value(1)

i = 0
while True:
    e = EPD_2in13_V3_Landscape()
    buf = bytearray(e.height * e.width // 8)
    fb = framebuf.FrameBuffer(buf, e.height, e.width, framebuf.MONO_VLSB)
    black = 0
    white = 1

    # fb.fill(white)
    # e.display_Partial(buf)
    # fb.text("zdarec'''", 10, 20, black)
    # e.display_Partial(buf)


    class NotionalDisplay(framebuf.FrameBuffer):
        def __init__(self, height, width, buffer):
            self.width = width
            self.height = height
            self.buffer = buffer
            self.mode = framebuf.MONO_VLSB
            super().__init__(self.buffer, self.width, self.height, self.mode)

        def show(self):
            ...

    my_display = NotionalDisplay(e.width, e.height, buf)
    wri = Writer(my_display, bigfont)
    wri.fgcolor = black
    wri.bgcolor = white

    Writer.set_textpos(my_display, 30, 5)
    temp = read_temp_1sens()
    disp_msg = str(temp).replace(".", ",") if temp is not None else "??.?"
    fb.fill(white)
    e.display_Partial(buf)
    wri.printstring(disp_msg, True)
    my_display.show()
    e.display_Partial(buf)

    adc_onboard_temperature = machine.ADC(4)
    ADC_voltage = adc_onboard_temperature.read_u16() * (3.3 / (65535))
    onboard_temperature = 27 - (ADC_voltage - 0.706) / 0.001721
    onboard_temperature = str(round(onboard_temperature, 1))
    print("Onboard emperature:", onboard_temperature, "°C")

    ssid = "Solar"
    password = "88888888"

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)    # Diable powersave mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    #Handle connection error
    if wlan.status() != 3:
        print('wifi connection failed')
        continue
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


    def connectMQTT():
        client = MQTTClient(client_id=b"bojler1",
                            server=b"192.168.43.37",
                            port=1883,
                            user=b"mqtt",
                            password=b"mqtt",
                            keepalive=7200,
                            ssl=False
                            )

        client.connect()
        return client

    try:
        client = connectMQTT()
    except Exception as e:
        print(e)
        continue

    def publish(topic, value):
        print(topic)
        print(value)
        client.publish(topic, value)
        print("publish Done")

    disp_msg = str(temp) if temp is not None else "null"

    try:
        publish("Bojler", '{"jimka": ' + disp_msg + '"ambient": ' + onboard_temperature + '}')
    except Exception as e:
        print(e)
        wlan.disconnect()
        continue

    # time.sleep(1)
    i += 1

    client.disconnect()
    wlan.disconnect()
    time.sleep(5)
