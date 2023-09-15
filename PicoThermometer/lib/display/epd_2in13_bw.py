from ssd_1680 import SSD1680
from time import sleep_ms

HEIGHT = 250
WIDTH = 128

SEEN_HEIGHT = 250
SEEN_WIDTH = 122

LEFT = 0
RIGHT = 249
TOP = 6
BOTTOM = 127


class Epd2in13bw(SSD1680):

    def __init__(self, busy, rst, dc, cs, spi):
        super().__init__(busy, rst, dc, cs, spi, HEIGHT, WIDTH)
        self.lut_partial = [
            0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x80, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x40, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x14, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0,
            0x22, 0x17, 0x41, 0x00, 0x32, 0x36,
        ]
        self.partial_in_use = False

    def show_full(self, data_black):
        if self.partial_in_use:
            self.epd_hw_init()
            self.partial_in_use = False

        self.send_command(0x24)
        for j in range(self.width_end_byte, -1, -1):
            for i in range(0, self.height):
                self.send_int_data(data_black[i + j * self.height])
        self.full_update()

    def send_lut(self):
        self.send_command(0x32)
        self.send_collection_data(self.lut_partial[0:153])
        self.wait_busy()

        self.send_command(0x3F)
        self.send_int_data(self.lut_partial[153])
        self.send_command(0x03)                     # gate voltage
        self.send_int_data(self.lut_partial[154])
        self.send_command(0x04)                     # source voltage
        self.send_int_data(self.lut_partial[155])   # VSH
        self.send_int_data(self.lut_partial[156])   # VSH2
        self.send_int_data(self.lut_partial[157])   # VSL
        self.send_command(0x2C)                     # VCOM
        self.send_int_data(self.lut_partial[158])

    def show_partial(self, image):

        self.reset.value(False)
        sleep_ms(1)
        self.reset.value(True)
        if not self.partial_in_use:
            self.send_lut()

            self.send_command(0x37)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x40)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x00)
            self.send_int_data(0x00)

            self.send_command(0x3C)
            self.send_int_data(0x80)

        self.send_command(0x22)
        self.send_int_data(0xC0)
        self.send_command(0x20)
        self.wait_busy()

        self._define_ram_area(0, 0, self.width - 1, self.height - 1)
        self._set_ram_pointer(0, 0)

        self.send_command(0x24)
        for j in range(self.width_end_byte, -1, -1):
            for i in range(0, self.height):
                self.send_int_data(image[i + j * self.height])

        self._update_partial()
        self.partial_in_use = True

    def _update_partial(self):
        """
        function : Turn On Display Part
        parameter:
        """
        self.send_command(0x22)  # Display Update Control
        self.send_int_data(0x0c)  # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence
        self.wait_busy()

    def load_previous(self, image):
        self.send_command(0x26)
        for j in range(self.width_end_byte, -1, -1):
            for i in range(0, self.height):
                self.send_int_data(image[i + j * self.height])
