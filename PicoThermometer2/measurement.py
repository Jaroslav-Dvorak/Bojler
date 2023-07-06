from lib.ds18x20 import DS18X20
from lib.onewire import OneWire
from time import sleep_ms


def measure_analog(pin):
    num_of_measurements = 1000
    n = 0
    measured = 0
    while n < num_of_measurements:
        measured += pin.read_u16()
        n += 1
    voltage = (measured / num_of_measurements) * (3.3 / 65535)
    return voltage


def measure_onewire(pin):
    ds_sensor = DS18X20(OneWire(pin))

    tries = 0
    while True:
        if tries > 100:
            return None

        tries += 1
        temp = None
        roms = ds_sensor.scan()
        if len(roms) == 0:
            print("no rom found")
            continue
        try:
            ds_sensor.convert_temp()
        except Exception as e:
            print(e)
            continue

        sleep_ms(750)

        for rom in roms:
            try:
                temp = ds_sensor.read_temp(rom)
            except Exception as e:
                print(e)
                continue

        if temp is None or temp == 85.0:
            continue
        temp = int(temp)
        return temp
