from ssd_1680 import SSD1680

HEIGHT_250 = 250
WIDTH_128 = 128

LEFT = 0
RIGHT = 249
TOP = 6
BOTTOM = 127


class Epd2in13brw(SSD1680):

    def __init__(self, busy, rst, dc, cs, spi):
        super().__init__(busy, rst, dc, cs, spi, HEIGHT_250, WIDTH_128)

    def show(self, data_black, data_red):
        self.send_command(0x24)
        for j in range(self.width_end_byte, -1, -1):
            for i in range(0, self.height):
                self.send_int_data(data_black[i + j * self.height])

        self.send_command(0x26)
        for j in range(self.width_end_byte, -1, -1):
            for i in range(0, self.height):
                self.send_int_data(data_red[i + j * self.height])
        self.full_update()

