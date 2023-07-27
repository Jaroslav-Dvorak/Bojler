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
        self.w = 249
        self.h = 119

    def clear(self, background):
        self.eink.Clear()
        self.eink.fill(background)

    def chart(self, values, maximum, minimum, color=0):
        left = -1
        right = self.w
        top = 0
        bottom = self.h

        # val = 66
        # norm = (val - minimum)/(maximum - minimum)
        # out = norm*(top-bottom)+bottom
        # values = [int(out)]*100
        optimized_values = [int(((val - minimum) / (maximum - minimum)) * ((bottom - top) + top)) for val in values]

        # self.eink.line(0, 0, w, 0, color)  # top horizontal
        # self.eink.line(0, h, w, h, color)  # bottom horizontal
        #

        self.eink.line(left+1, top, left+1, bottom, color)  # left vertical
        self.eink.line(left+2, top, left+2, bottom, color)  # left vertical
        self.eink.line(left+3, top, left+3, bottom, color)  # left vertical
        # self.eink.line(w, h, w, 0, color)  # right vertical

        spread = 1
        for index, _ in enumerate(optimized_values, start=1):
            value = optimized_values[-index]
            y1 = bottom - value
            x1 = right - index*spread
            x2 = right - ((index*spread)+spread)
            try:
                value = optimized_values[-index - 1]
                y2 = bottom - value
            except IndexError:
                break

            # print("x1:", x1, " y1:", y1)
            # print("x2:", x2, " y2:", y2)
            self.eink.line(x1, y1, x2, y2, color)

        self.eink.line(left+4, top, left+4, bottom, not color)  # left vertical
        self.eink.line(left+5, top, left+5, bottom, not color)  # left vertical

        self.eink.fill_rect(left+6, top, left+20, top+10, not color)
        self.eink.text(str(maximum), left+7, top, color)
        self.eink.fill_rect(left+6, bottom-10, left+20, bottom-20, not color)
        self.eink.text(str(minimum), left+7, bottom-7, color)

        self.eink.fill_rect(right-40, top, right, top+15, not color)
        self.eink.text(str(values[-1]), right-35, top, color)

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

