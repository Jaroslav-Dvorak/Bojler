from time import sleep_ms

HEIGHT_250 = 250
WIDTH_128 = 128
WIDTH_END_BYTE = 15     # (WIDTH_128 // 8 - 1)
HEIGHT_END_BIT = 249    # (HEIGHT_250 - 1)

LEFT = 0
RIGHT = 249
TOP = 6
BOTTOM = 127


class GDEY0213Z98:
    def __init__(self, busy, rst, dc, cs, spi, border):
        self.busy = busy
        self.reset = rst
        self.dc = dc
        self.cs = cs
        self.spi = spi

        self.border = border
        self.epd_hw_init()

    def spi_write(self, value):
        self.spi.write(bytearray(value))

    def send_command(self, command):
        self.cs.value(False)
        self.dc.value(False)
        self.spi_write([command])
        self.cs.value(True)

    def send_data(self, data):
        self.cs.value(False)
        self.dc.value(True)
        self.spi_write([data])
        self.cs.value(True)

    def write_array_data(self, arr):
        self.cs.value(False)
        self.dc.value(True)
        self.spi_write(arr)
        self.cs.value(True)

    def wait_busy(self):
        while self.busy.value():
            sleep_ms(3)

    def epd_hw_init(self):
        # Module reset
        self.reset.value(False)
        sleep_ms(10)
        self.reset.value(True)
        sleep_ms(10)

        # SWRESET
        self.wait_busy()
        self.send_command(0x12)
        self.wait_busy()

        # Driver output control
        self.send_command(0x01)
        self.send_data(HEIGHT_END_BIT % 256)
        self.send_data(HEIGHT_END_BIT // 256)
        self.send_data(0x00)

        # data entry mode
        self.send_command(0x11)
        self.send_data(0b00000111)

        # set Ram - X address start / end position
        self.send_command(0x44)
        self.send_data(0x00)
        self.send_data(WIDTH_END_BYTE)

        # set Ram - Y address start / end position
        self.send_command(0x45)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(HEIGHT_END_BIT % 256)
        self.send_data(HEIGHT_END_BIT // 256)

        # set RAM x address count to 0
        self.send_data(WIDTH_END_BYTE)
        self.send_command(0x4E)

        # set RAM y address count to 0X199;
        self.send_command(0x4F)
        self.send_data(0x00)
        self.send_data(0x00)

        # BorderWaveform
        self.send_command(0x3C)
        self.send_data(0b00000100 | self.border)  # 00 - black, 01 - white, 10 and 11 - red

        # Display update control
        self.send_command(0x21)
        self.send_data(0x00)
        self.send_data(0x80)

        # Read built - in temperature sensor
        self.send_command(0x18)
        self.send_data(0x80)

        self.wait_busy()

    def deep_sleep(self):
        self.send_command(0x10)  # enter deep sleep
        self.send_data(0x01)
        sleep_ms(100)

    def full_update(self):
        # Display Update Control
        self.send_command(0x22)
        self.send_data(0xF7)
        # Activate Display Update Sequence
        self.send_command(0x20)
        self.wait_busy()

    def show(self, data_black, data_red):
        self.send_command(0x24)        # Transfer old data
        # self.write_array_data(data_black)
        for j in range(WIDTH_END_BYTE, -1, -1):
            for i in range(0, HEIGHT_250):
                self.send_data(data_black[i + j * HEIGHT_250])
        # for data in data_black:
        #     self.send_data(data)  # Transfer the actual displayed data

        self.send_command(0x26)        # Transfer new data
        # self.write_array_data(data_red)
        for j in range(WIDTH_END_BYTE, -1, -1):
            for i in range(0, HEIGHT_250):
                self.send_data(data_red[i + j * HEIGHT_250])
        # for data in data_red:
        #     self.send_data(data)  # Transfer the actual displayed data
        #     self.send_data(~data)    # Transfer the actual displayed data
        self.full_update()

    def show_straight(self, data_black, data_red):
        self.send_command(0x24)        # Transfer old data
        self.write_array_data(data_black)
        self.send_command(0x26)        # Transfer new data
        self.write_array_data(data_red)
        self.full_update()

    def white_screen(self):
        num_of_bytes = (WIDTH_128 * HEIGHT_250) // 8
        self.send_command(0x24)        # Transfer old data
        for i in range(num_of_bytes):
            self.send_data(0xFF)  # Transfer the actual displayed data

        self.send_command(0x26)        # Transfer new data
        for i in range(num_of_bytes):
            self.send_data(0x00)    # Transfer the actual displayed data

        self.full_update()
