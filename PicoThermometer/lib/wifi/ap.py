from time import sleep
from gpio_definitions import GREEN_LED
import usocket as socket
import network

AP = network.WLAN(network.AP_IF)
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object


def start_ap(ssid):
    AP.config(security=0, ssid=ssid)
    AP.active(True)

    while not AP.active():
        pass
    ip = AP.ifconfig()[0]
    return ip


def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body><h1>Welcome to microcontrollerslab!</h1></body></html>"""
    return html


def start_web():
    S.bind(('', 80))
    S.listen(5)
    while True:
        conn, addr = S.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        response = web_page()
        conn.send(response)
        conn.close()
