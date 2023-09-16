import framebuf
from writer import Writer
import bigfont
from epd_2in13_brw import HEIGHT_250, WIDTH_128, BOTTOM, TOP

WHITE = 1
BLACK = 0
RED = 2


class Drawing:
    def __init__(self, background=WHITE):
        self.background = background

        self.buffer_black = bytearray(HEIGHT_250 * WIDTH_128 // 8)
        self.buffer_red = bytearray(HEIGHT_250 * WIDTH_128 // 8)
        self.canvas_black = framebuf.FrameBuffer(self.buffer_black, HEIGHT_250, WIDTH_128, framebuf.MONO_VLSB)
        self.canvas_red = framebuf.FrameBuffer(self.buffer_red, HEIGHT_250, WIDTH_128, framebuf.MONO_VLSB)

        if background == WHITE:
            self.canvas_black.fill(1)
            self.canvas_red.fill(0)
            fill_black = b"\xFF"
            fill_red = b"\x00"
        elif background == BLACK:
            self.canvas_black.fill(0)
            self.canvas_red.fill(0)
            fill_black = b"\x00"
            fill_red = b"\x00"
        else:   # background == RED:
            self.canvas_black.fill(1)
            self.canvas_red.fill(1)
            fill_black = b"\xFF"
            fill_red = b"\xFF"

    def color_decider(self, color):
        if self.background == WHITE:
            if color == BLACK:
                return (self.canvas_red, 0, False), (self.canvas_black, 0, True),
            elif color == RED:
                return ((self.canvas_red, 1, False),)
            else:
                return (self.canvas_red, 0, False), (self.canvas_black, 1, True),
        elif self.background == BLACK:
            if color == WHITE:
                return (self.canvas_red, 0, False), (self.canvas_black, 1, False)
            elif color == RED:
                return ((self.canvas_red, 1, False),)
            else:
                return (self.canvas_red, 0, False), (self.canvas_black, 0, True)
        else:   # self.background == RED:
            if color == BLACK:
                return (self.canvas_red, 0, True), (self.canvas_black, 0, True)
            else:   # color == WHITE:
                return (self.canvas_red, 0, True), (self.canvas_black, 1, False)

    def pixel(self, x, y, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.pixel(x, y, color_value)

    def line(self, x1, y1, x2, y2, color=BLACK):
        y1 += TOP
        y2 += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.line(x1, y1, x2, y2, color_value)

    def hline(self, x, y, w, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.hline(x, y, w, color_value)

    def vline(self, x, y, h, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.vline(x, y, h, color_value)

    def rect(self, x, y, w, h, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.rect(x, y, w, h, color_value)

    def fill_rect(self, x, y, w, h, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.fill_rect(x, y, w, h, color_value)

    def circle(self, x, y, radius, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            f = 1 - radius
            ddf_x = 1
            ddf_y = -2 * radius
            x_r = 0
            y_r = radius
            canvas.pixel(x, y + radius, color_value)  # bottom
            canvas.pixel(x, y - radius, color_value)  # top
            canvas.pixel(x + radius, y, color_value)  # right
            canvas.pixel(x - radius, y, color_value)  # left
            while x_r < y_r:
                if f >= 0:
                    y_r -= 1
                    ddf_y += 2
                    f += ddf_y
                x_r += 1
                ddf_x += 2
                f += ddf_x
                # angle notations are based on the unit circle and in diection of being drawn
                canvas.pixel(x + x_r, y + y_r, color_value)  # 270 to 315
                canvas.pixel(x - x_r, y + y_r, color_value)  # 270 to 255
                canvas.pixel(x + x_r, y - y_r, color_value)  # 90 to 45
                canvas.pixel(x - x_r, y - y_r, color_value)  # 90 to 135
                canvas.pixel(x + y_r, y + x_r, color_value)  # 0 to 315
                canvas.pixel(x - y_r, y + x_r, color_value)  # 180 to 225
                canvas.pixel(x + y_r, y - x_r, color_value)  # 0 to 45
                canvas.pixel(x - y_r, y - x_r, color_value)  # 180 to 135

    def fill_circle(self, x, y, radius, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.vline(x, y - radius, 2 * radius + 1, color_value)
            f = 1 - radius
            ddf_x = 1
            ddf_y = -2 * radius
            x_r = 0
            y_r = radius
            while x_r < y_r:
                if f >= 0:
                    y_r -= 1
                    ddf_y += 2
                    f += ddf_y
                x_r += 1
                ddf_x += 2
                f += ddf_x
                canvas.vline(x + x_r, y - y_r, 2 * y_r + 1, color_value)
                canvas.vline(x + y_r, y - x_r, 2 * x_r + 1, color_value)
                canvas.vline(x - x_r, y - y_r, 2 * y_r + 1, color_value)
                canvas.vline(x - y_r, y - x_r, 2 * x_r + 1, color_value)

    def tiny_text(self, string, x, y, color=BLACK):
        y += TOP
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.text(string, x, y, color_value)

    def large_text(self, string, x, y, color=BLACK):
        x -= 4
        for decided in self.color_decider(color):
            canvas, color_value, invert = decided
            writer_inst = Writer(canvas, WIDTH_128, HEIGHT_250, bigfont)
            writer_inst.fgcolor = color_value
            writer_inst.bgcolor = not color_value
            writer_inst.set_textpos(TOP, x)
            writer_inst.y_offset = y
            writer_inst.printstring(string, invert)
