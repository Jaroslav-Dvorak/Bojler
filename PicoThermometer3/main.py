from lib.gdey0213z98 import GDEY0213Z98
# from pict import *
from time import sleep
from gpio_definitions import *
from display.widgets import Widgets, WHITE, RED, BLACK
import nonvolatile
import measurement

background = WHITE

Left = 0
Right = 249
Top = 0
Bottom = 121

# viz.tiny_text("zdar zdar zdarau cus", Left, Top - 20, BLACK)
# viz.tiny_text("CHRRRRRST", Left, Bottom + 8, 2)
#
# viz.line(Left, Bottom, Right, Bottom, RED)
# viz.line(Left, Top, Left, Bottom, RED)
# viz.line(Right, Top, Right, Bottom, RED)
# viz.line(Left, Top, Right, Top, RED)
# #
# viz.line(Left, Top, Right, Bottom, 2)
# viz.line(Left, Bottom, Right, Top, 2)

# viz.rect(66, 80, 50, 70)
# viz.fill_rect(140, 33, 50, 70, 2)
# viz.large_text("21.3", 0, 0, BLACK)
# viz.canvas_black.text("zdar jak pes", 0, 0)
# viz.canvas_red.text("RED RED RED", 0, 30)

# epd_hw_init(rotation=False)   # Full screen refresh initialization.
# EPD_WhiteScreen_ALL(gImage_BW1, gImage_RW1)     # To Display one image using full screen refresh.

while True:
    temper_onboard_voltage = measurement.measure_analog(TEMPER_ADC)
    onboard_temperature = 27 - (temper_onboard_voltage - 0.706) / 0.001721
    optimized_temp = int((onboard_temperature - 25) * 10)
    if optimized_temp < -127:
        optimized_temp = -127
    elif optimized_temp > 128:
        optimized_temp = 128
    temperatures = nonvolatile.save_and_get_last_values(optimized_temp, "temperatures.dat")
    temperatures = [temp / 10 + 25 for temp in temperatures]

    viz = Widgets()
    viz.chart(temperatures, minimum=15, maximum=35)

    bat_voltage = measurement.measure_analog(BATT_ADC) * 2
    # soc = int((1 - ((4.0 - bat_voltage)/1.5)) * 100)
    # soc = 0 if soc < 0 else soc
    bat_voltage = str(round(bat_voltage, 2)) + "V"
    viz.tiny_text(bat_voltage, 60, Top)
    #
    # viz.fill_circle(90, 30, 40, RED)
    # viz.circle(40, 60, 60, WHITE)

    eink = GDEY0213Z98(busy=BUSY_PIN, rst=RST_PIN, dc=DC_PIN, cs=CS_PIN, spi=SPI, border=background)
    # eink.show_straight(gImage_BW1, gImage_RW1)     # To Display one image using full screen refresh.
    eink.show(viz.buffer_black, viz.buffer_red)     # To Display one image using full screen refresh.

    eink.deep_sleep()     # Enter the sleep mode and please do not delete it, otherwise it will reduce the lifespan of the screen.\

    sleep(1)
    DONE_PIN.value(1)
    sleep(10)
