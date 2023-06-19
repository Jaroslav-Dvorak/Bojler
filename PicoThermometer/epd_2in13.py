from machine import Pin, SPI
import framebuf
import utime
import machine

EPD_WIDTH = 122
EPD_HEIGHT = 250

SCL_PIN = machine.Pin(2)    # SCL=SCK
SDA_PIN = machine.Pin(3)    # SDA=MOSI
CS_PIN = 4
vcc_pin = machine.Pin(5, machine.Pin.OUT).value(1)
DC_PIN = 6
RST_PIN = 7
BUSY_PIN = 8

WF_PARTIAL_2IN13_V3 = [
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

WS_20_30_2IN13_V3 = [
    0x80, 0x4A, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x40, 0x4A, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x80, 0x4A, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x40, 0x4A, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0xF, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0xF, 0x0, 0x0, 0xF, 0x0, 0x0, 0x2,
    0xF, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0,
    0x22, 0x17, 0x41, 0x0, 0x32, 0x36
]


class EPD_2in13_V3_Landscape(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else:
            self.width = (EPD_WIDTH // 8) * 8 + 8

        self.height = EPD_HEIGHT

        self.full_lut = WF_PARTIAL_2IN13_V3
        self.partial_lut = WS_20_30_2IN13_V3

        self.spi = SPI(0, baudrate=4000_000, sck=SCL_PIN, mosi=SDA_PIN)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.height, self.width, framebuf.MONO_VLSB)
        self.init()

    def digital_write(self, pin, value):
        '''
        function :Change the pin state
        parameter:
            pin : pin
            value : state
        '''
        pin.value(value)

    def digital_read(self, pin):
        '''
        function : Read the pin state
        parameter:
            pin : pin
        '''
        return pin.value()

    def delay_ms(self, delaytime):
        '''
        function : The time delay function
        parameter:
            delaytime : ms
        '''
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        '''
        function : Write data to SPI
        parameter:
            data : data
        '''
        self.spi.write(bytearray(data))

    def reset(self):
        '''
        function :Hardware reset
        parameter:
        '''
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)

    def send_command(self, command):
        '''
        function :send command
        parameter:
         command : Command register
        '''
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        '''
        function :send data
        parameter:
         data : Write data
        '''
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        '''
        function :Wait until the busy_pin goes LOW
        parameter:
        '''
        print('busy')
        self.delay_ms(10)
        while (self.digital_read(self.busy_pin) == 1):  # 0: idle, 1: busy
            self.delay_ms(10)
        print('busy release')

    def TurnOnDisplay(self):
        '''
        function : Turn On Display
        parameter:
        '''

        self.send_command(0x22)  # Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def TurnOnDisplayPart(self):
        '''
        function : Turn On Display Part
        parameter:
        '''
        self.send_command(0x22)  # Display Update Control
        self.send_data(0x0F)  # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def LUT(self, lut):
        '''
        function : Set lut
        parameter:
            lut : lut data
        '''
        self.send_command(0x32)
        self.send_data1(lut[0:153])
        self.ReadBusy()

    def LUT_by_host(self, lut):
        '''
        function : Send lut data and configuration
        parameter:
            lut : lut data
        '''
        self.LUT(lut)  # lut
        self.send_command(0x3F)
        self.send_data(lut[153])
        self.send_command(0x03)  # gate voltage
        self.send_data(lut[154])
        self.send_command(0x04)  # source voltage
        self.send_data(lut[155])  # VSH
        self.send_data(lut[156])  # VSH2
        self.send_data(lut[157])  # VSL
        self.send_command(0x2C)  # VCOM
        self.send_data(lut[158])

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        '''
        function : Setting the display window
        parameter:
            Xstart : X-axis starting position
            Ystart : Y-axis starting position
            Xend : End position of X-axis
            Yend : End position of Y-axis
        '''
        self.send_command(0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart >> 3) & 0xFF)
        self.send_data((Xend >> 3) & 0xFF)

        self.send_command(0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)

    def SetCursor(self, Xstart, Ystart):
        '''
        function : Set Cursor
        parameter:
            Xstart : X-axis starting position
            Ystart : Y-axis starting position
        '''
        self.send_command(0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)

        self.send_command(0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)

    def init(self):
        '''
        function : Initialize the e-Paper register
        parameter:
        '''
        print('init')
        self.reset()
        self.delay_ms(100)

        self.ReadBusy()
        self.send_command(0x12)  # SWRESET
        self.ReadBusy()

        self.send_command(0x01)  # Driver output control
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x07)

        self.SetWindows(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x3C)  # BorderWaveform
        self.send_data(0x05)

        self.send_command(0x21)  # Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.send_command(0x18)  # Read built-in temperature sensor
        self.send_data(0x80)

        self.ReadBusy()
        self.LUT_by_host(self.partial_lut)

    def Clear(self):
        '''
        function : Clear screen
        parameter:
        '''
        self.send_command(0x24)
        self.send_data1([0xff] * self.height * int(self.width / 8))

        self.TurnOnDisplay()

    def display(self, image):
        '''
        function : Sends the image buffer in RAM to e-Paper and displays
        parameter:
            image : Image data
        '''
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplay()

    def Display_Base(self, image):
        '''
        function : Refresh a base image
        parameter:
            image : Image data
        '''
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.send_command(0x26)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplay()

    def display_Partial(self, image):
        '''
        function : Sends the image buffer in RAM to e-Paper and partial refresh
        parameter:
            image : Image data
        '''
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(1)
        self.digital_write(self.reset_pin, 1)

        self.LUT_by_host(self.full_lut)

        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x3C)
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.ReadBusy()

        self.SetWindows(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)

        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplayPart()

    def sleep(self):
        '''
        function : Enter sleep mode
        parameter:
        '''
        self.send_command(0x10)  # enter deep sleep
        self.send_data(0x01)
        self.delay_ms(100)

    # epd = EPD_2in13_V3_Portrait()
    # epd.Clear()
    #
    # epd.fill(0xff)
    # epd.text("Waveshare", 0, 10, 0x00)
    # epd.text("ePaper-2.13_V3", 0, 30, 0x00)
    # epd.text("Raspberry Pico", 0, 50, 0x00)
    # epd.text("Hello World", 0, 70, 0x00)
    # epd.display(epd.buffer)
    # epd.delay_ms(2000)
    #
    # epd.vline(10, 90, 60, 0x00)
    # epd.vline(90, 90, 60, 0x00)
    # epd.hline(10, 90, 80, 0x00)
    # epd.hline(10, 150, 80, 0x00)
    # epd.line(10, 90, 90, 150, 0x00)
    # epd.line(90, 90, 10, 150, 0x00)
    # epd.display(epd.buffer)
    # epd.delay_ms(2000)
    #
    # epd.rect(10, 180, 50, 40, 0x00)
    # epd.fill_rect(60, 180, 50, 40, 0x00)
    # epd.Display_Base(epd.buffer)
    # epd.delay_ms(2000)
    #
    # epd.init()
    # for i in range(0, 10):
    #     epd.fill_rect(40, 230, 40, 10, 0xff)
    #     epd.text(str(i), 60, 230, 0x00)
    #     epd.display_Partial(epd.buffer)
    #
    # print("sleep")
    # epd.init()
    # epd.Clear()
    # epd.delay_ms(2000)
    # epd.sleep()
