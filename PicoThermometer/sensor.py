
# _____________________DS18X20_____________________________________________________
# from lib.ds18x20 import DS18X20
# from lib.onewire import OneWire
# from machine import Pin
# DALLAS = Pin(19)
# ds18x20 = DS18X20(OneWire(DALLAS))
# sensor_settings = OrderedDict()
# sensor_settings["Minimum"] = 0
# sensor_settings["Maximum"] = 70
#
# def get_serial():
#     tries = 0
#     while True:
#         if tries > 100:
#             return False
#         tries += 1
#         roms = ds18x20.scan()
#         if len(roms) > 0:
#             return ''.join([byte.to_bytes(1, 'big').hex() for byte in roms[0]])
#
#
# def get_values():
#     from nonvolatile import Settings
#     rom = Settings["dallas_sens"]
#     rom = bytes.fromhex(rom)
#     try:
#         ds18x20.convert_temp()
#         sleep_ms(750)
#         temp = ds18x20.read_temp(rom)
#     except Exception as e:
#         print(e)
#         return False
#     else:
#         values = OrderedDict()
#         values["temperature"] = round(temp, 1)
#         return values
#
#
# def get_range():
#     from nonvolatile import Settings
#     return Settings["Minimum"], Settings["Maximum"]
#
#
# def set_sensor():
#     pass

# _____________________SCD4X_____________________________________________________

from lib.scd4x import SCD4X
from machine import I2C, Pin


i2c_id = 0
i2c = I2C(i2c_id, scl=Pin(9), sda=Pin(8), freq=400_000)
sensor = SCD4X(i2c_bus=i2c)

# scd4x = SCD4X(I2c)

# sensor_settings = OrderedDict()
# sensor_settings["Altitude"] = scd4x.altitude


# def get_serial():
#     serial_number = scd4x.serial_number
#     if not all(not v for v in serial_number):
#         return serial_number
#     else:
#         return False


# def get_values():
#     global scd4x
#     scd4x.measure_single_shot()
#     values = OrderedDict()
#     values["co2"] = scd4x.co2
#     values["temperature"] = scd4x.temperature
#     values["humidity"] = scd4x.relative_humidity
#
#     # values["co2"] = 0
#     # values["temperature"] = 0
#     # values["humidity"] = 0
#     return values


# def get_range():
#     return 400, 5000
#
#
# def setup_sensor():
#     from nonvolatile import Settings
#     scd4x.altitude = Settings["Altitude"]
