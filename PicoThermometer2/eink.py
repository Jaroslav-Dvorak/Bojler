import framebuf
from lib.writer import Writer
from lib import bigfont
from gpio_definitions import *
from lib.epd_2in9_wb import EPD_2in9_Portrait, NotionalDisplay


class Eink:
    def __init__(self):
        self.eink = EPD_2in9_Portrait(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SDA_PIN, SCL_PIN, SPI_NUM)
        self.buf = bytearray(self.eink.height * self.eink.width // 8)
        self.fb = framebuf.FrameBuffer(self.buf, self.eink.width, self.eink.height, framebuf.MONO_HLSB)
        self.black = 0
        self.white = 1

        self.my_display = NotionalDisplay(self.eink.width, self.eink.height, self.buf)
        self.wri = Writer(self.my_display, bigfont)
        self.wri.fgcolor = self.black
        self.wri.bgcolor = self.white

        self.fb.fill(self.white)

    def clear(self):
        self.eink.Clear(0xff)

    def show(self, num_1, num_2, num_3, num_4, bar):
        temperatures = [num_1, num_2, num_3, num_4]
        for i, y in enumerate(range(0, 250, 75)):
            x = 0

            if temperatures[i] is None:
                msg = "--"
            elif -50 < temperatures[i] < 10:
                x = 30
                msg = str(int(temperatures[i]))
            else:
                msg = str(int(temperatures[i]))
            Writer.set_textpos(self.my_display, y, x)
            self.wri.printstring(msg, True)

        self.my_display.show()
        x, y, w, h = 117, 2, 10, 292
        self.fb.rect(x, y, w, h, self.black)

        bar *= h / 100
        bar = int(bar)
        y = h - bar + 1
        h = bar

        self.fb.fill_rect(x, y, w, h, self.black)
        self.eink.display_Base(self.buf)


def show(num_1, num_2, num_3, num_4, bar):
    eink = EPD_2in9_Portrait(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SDA_PIN, SCL_PIN, SPI_NUM)

    buf = bytearray(eink.height * eink.width // 8)
    fb = framebuf.FrameBuffer(buf, eink.width, eink.height, framebuf.MONO_HLSB)
    black = 0
    white = 1

    my_display = NotionalDisplay(eink.width, eink.height, buf)
    wri = Writer(my_display, bigfont)
    wri.fgcolor = black
    wri.bgcolor = white

    fb.fill(white)

    eink.Clear(0xff)

    temperatures = [num_1, num_2, num_3, num_4]
    for i, y in enumerate(range(0, 250, 75)):
        x = 0

        if temperatures[i] is None:
            msg = "--"
        elif -50 < temperatures[i] < 10:
            x = 30
            msg = str(int(temperatures[i]))
        else:
            msg = str(int(temperatures[i]))
        Writer.set_textpos(my_display, y, x)
        wri.printstring(msg, True)

    my_display.show()
    x, y, w, h = 117, 2, 10, 292
    fb.rect(x, y, w, h, black)

    bar *= h/100
    bar = int(bar)
    y = h-bar+1
    h = bar

    fb.fill_rect(x, y, w, h, black)
    eink.display_Base(buf)
