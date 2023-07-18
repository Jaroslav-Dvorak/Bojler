import framebuf
from lib.writer import Writer
from lib import bigfont
from gpio_definitions import *
from lib.epd_2in13 import EPD_2in13_V3_Landscape, NotionalDisplay


class Eink:
    def __init__(self):
        self.eink = EPD_2in13_V3_Landscape(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SDA_PIN, SCL_PIN, SPI_NUM)
        self.buf = bytearray(self.eink.width * self.eink.height // 8)
        self.fb = framebuf.FrameBuffer(self.buf, self.eink.height, self.eink.width, framebuf.MONO_VLSB)
        self.black = 0
        self.white = 1

        self.my_display = NotionalDisplay(self.eink.width, self.eink.height, self.buf)
        self.wri = Writer(self.my_display, bigfont)
        self.wri.fgcolor = self.black
        self.wri.bgcolor = self.white

        self.fb.fill(self.white)

    def clear(self):
        self.eink.Clear()

    def show(self, num_1):

        # temperatures = [num_1]
        # for i, y in enumerate(range(0, 250, 75)):
        #     x = 0
        #
        #     if temperatures[i] is None:
        #         msg = "--"
        #     elif -50 < temperatures[i] < 10:
        #         x = 30
        #         msg = str(int(temperatures[i]))
        #     else:
        #         msg = str(int(temperatures[i]))

            # Writer.set_textpos(self.my_display, y, x)
            # self.wri.printstring(msg, True)

        msg = str(num_1)
        Writer.set_textpos(self.my_display, 30, 5)
        self.wri.printstring(msg, True)

        self.my_display.show()
        # x, y, w, h = 117, 2, 10, 292
        # self.fb.rect(x, y, w, h, self.black)

        self.eink.display(self.buf)

