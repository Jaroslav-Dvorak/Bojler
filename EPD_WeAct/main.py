from drawing_bw import Drawing, BLACK, WHITE
# from epd_2in13_BRW import Epd2in13brw, HEIGHT_250, WIDTH_128
from epd_2in13_bw import Epd2in13bw, HEIGHT_250, WIDTH_128
from gpio_definitions import *
from time import sleep_ms

Left = 0
Right = 249
Top = 0
Bottom = 121

draw = Drawing(background=WHITE)
epd = Epd2in13bw(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI)

draw.circle(100, 60, 60)
epd.load_previous(draw.img)

size = 10
for x in range(0, HEIGHT_250, size):
    draw.clear()
    draw.fill_rect(x, 0, size, size)
    epd.show_partial(draw.img)

draw.clear()
draw.circle(100, 60, 60)
epd.show_full(draw.img)

epd.deep_sleep()
