# from lib.ds18x20 import DS18X20
# from lib.onewire import OneWire
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


# class MeasureOnewire:
#     def __init__(self, pin, rom):
#         self.ds_sensor = DS18X20(OneWire(pin))
#         self.rom = rom
#
#     def convert(self):
#         tries = 0
#         while tries < 100:
#             try:
#                 self.ds_sensor.convert_temp()
#             except Exception as e:
#                 print(e)
#             tries += 1
#
#     def get_temp(self):
#         tries = 0
#         temp = None
#         while tries < 100:
#             tries += 1
#             try:
#                 temp = self.ds_sensor.read_temp(self.rom)
#             except Exception as e:
#                 print(e)
#                 continue
#
#             if temp is None or temp == 85.0:
#                 continue
#             else:
#                 break
#         return temp
#
#
# def measure_onewire(pin):
#     ds_sensor = DS18X20(OneWire(pin))
#
#     tries = 0
#     while True:
#         if tries > 100:
#             return None
#
#         tries += 1
#         temp = None
#         roms = ds_sensor.scan()
#         if len(roms) == 0:
#             print("no rom found")
#             continue
#         try:
#             ds_sensor.convert_temp()
#         except Exception as e:
#             print(e)
#             continue
#
#         sleep_ms(750)
#
#         for rom in roms:
#             try:
#                 temp = ds_sensor.read_temp(rom)
#             except Exception as e:
#                 print(e)
#                 continue
#
#         if temp is None or temp == 85.0:
#             continue
#
#         return temp
