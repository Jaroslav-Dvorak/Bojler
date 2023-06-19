# DS18x20 temperature sensor driver for MicroPython.
# MIT license; Copyright (c) 2016 Damien P. George

import time
from micropython import const
from machine import Pin
from onewire import OneWire

_CONVERT = const(0x44)
_RD_SCRATCH = const(0xBE)
_WR_SCRATCH = const(0x4E)


class DS18X20:
    def __init__(self, onewire):
        self.ow = onewire
        self.buf = bytearray(9)

    def scan(self):
        return [rom for rom in self.ow.scan() if rom[0] in (0x10, 0x22, 0x28)]

    def convert_temp(self):
        self.ow.reset(True)
        self.ow.writebyte(self.ow.SKIP_ROM)
        self.ow.writebyte(_CONVERT)

    def read_scratch(self, rom):
        self.ow.reset(True)
        self.ow.select_rom(rom)
        self.ow.writebyte(_RD_SCRATCH)
        self.ow.readinto(self.buf)
        if self.ow.crc8(self.buf):
            raise Exception("CRC error")
        return self.buf

    def write_scratch(self, rom, buf):
        self.ow.reset(True)
        self.ow.select_rom(rom)
        self.ow.writebyte(_WR_SCRATCH)
        self.ow.write(buf)

    def read_temp(self, rom):
        buf = self.read_scratch(rom)
        if rom[0] == 0x10:
            if buf[1]:
                t = buf[0] >> 1 | 0x80
                t = -((~t + 1) & 0xFF)
            else:
                t = buf[0] >> 1
            return t - 0.25 + (buf[7] - buf[6]) / buf[7]
        else:
            t = buf[1] << 8 | buf[0]
            if t & 0x8000:  # sign bit set
                t = -((t ^ 0xFFFF) + 1)
            return t / 16


ds_pin = Pin(0)
ds_sensor = DS18X20(OneWire(ds_pin))


def read_temp_1sens():
    tries = 0
    while True:
        if tries > 100:
            return "??.?"

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

        time.sleep_ms(750)

        for rom in roms:
            try:
                temp = ds_sensor.read_temp(rom)
            except Exception as e:
                print(e)
                continue

        if temp is None or temp == 85.0:
            continue
        temp = round(temp, 1)
        return temp

