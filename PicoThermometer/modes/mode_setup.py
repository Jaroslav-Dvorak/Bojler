from lib.wifi.ap import start_ap, start_web
from lib.display import screens
from measurement import Bat_voltage


def start_setup(ap_ssid):
    ip = start_ap(ap_ssid)
    screens.show_overview(Bat_voltage, ip, ap_ssid)
    start_web()
