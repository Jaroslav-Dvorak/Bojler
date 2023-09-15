from drawing_bw import Drawing, BLACK, WHITE
# from epd_2in13_BRW import Epd2in13brw, HEIGHT_250, WIDTH_128
from epd_2in13_bw import Epd2in13bw, HEIGHT_250, WIDTH_128
from gpio_definitions import *
from time import sleep_ms

Left = 0
Right = 249
Top = 0
Bottom = 121

# BLACK = not BLACK
# WHITE = not WHITE

draw = Drawing(background=WHITE)
epd = Epd2in13bw(BUSY_PIN, RST_PIN, DC_PIN, CS_PIN, SPI)

draw.large_text("12.5", 0, 0, BLACK)

epd.show(draw.img)

# for _ in range(3):
#     draw.hline(150, 66, 8, WHITE)
#     epd.show_partial(draw.img)
#     draw.hline(150, 66, 8, BLACK)
#     epd.show_partial(draw.img)
#
# draw.line(Left, Bottom, Right, Bottom, BLACK)
# draw.line(Left, Top, Left, Bottom, BLACK)
# draw.line(Right, Top, Right, Bottom, BLACK)
# draw.line(Left, Top, Right, Top, BLACK)
# epd.show(draw.img)
#
# for _ in range(3):
#     draw.hline(150, 66, 8, BLACK)
#     epd.show_partial(draw.img)
#     draw.hline(150, 66, 8, WHITE)
#     epd.show_partial(draw.img)

# draw.hline(150, 66, 8, BLACK)
# epd.show_partial(draw.img)

# sleep_ms(1000)
# canvas_black.text("cos", 66, 20, 0)
# epd.show_partial(buffer_black)

epd.deep_sleep()



