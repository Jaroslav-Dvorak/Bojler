import framebuf
from lib.writer import Writer
from lib import bigfont
from gpio_definitions import *
from lib.epd_2in9_wb import EPD_2in9_Portrait, NotionalDisplay

eink = EPD_2in9_Portrait(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SDA_PIN, SCL_PIN, SPI_NUM)


def show(num_1, num_2, num_3, num_4, bar):

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
            msg = str(temperatures[i])
        else:
            msg = str(temperatures[i])
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
