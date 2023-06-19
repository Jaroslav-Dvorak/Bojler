from epd_2in13 import EPD_2in13_V3_Landscape
import time
import machine
import onewire
import ds18x20
from writer import Writer
import bigfont
import framebuf


if __name__ == '__main__':

    vcc_pin = machine.Pin(1, machine.Pin.OUT)
    vcc_pin.value(1)
    ds_pin = machine.Pin(0)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    while True:
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
        msg = str(temp).replace(".", ",")
        fb.fill(white)
        e.display_Partial(buf)
        wri.printstring(msg, True)
        my_display.show()
        e.display_Partial(buf)
