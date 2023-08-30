import framebuf
from writer import Writer
import bigfont
from gdey0213z98 import HEIGHT_250, WIDTH_128, BOTTOM, TOP, LEFT, RIGHT


WHITE = 1
BLACK = 0
RED = 2


class Vizualizer:
    def __init__(self, background=WHITE):
        if background == WHITE:
            fill_black = b"\xFF"
            fill_red = b"\x00"
        elif background == BLACK:
            fill_black = b"\x00"
            fill_red = b"\x00"
        else:   # background == RED:
            fill_black = b"\xFF"
            fill_red = b"\xFF"
        self.background = background

        self.buffer_black = bytearray(fill_black * (HEIGHT_250 * WIDTH_128 // 8))
        self.buffer_red = bytearray(fill_red * (HEIGHT_250 * WIDTH_128 // 8))
        self.canvas_black = framebuf.FrameBuffer(self.buffer_black, HEIGHT_250, WIDTH_128, framebuf.MONO_VLSB)
        self.canvas_red = framebuf.FrameBuffer(self.buffer_red, HEIGHT_250, WIDTH_128, framebuf.MONO_VLSB)

    def color_decider(self, color):
        if self.background == WHITE:
            if color == BLACK:
                return ((self.canvas_black, 0, True),)
            elif color == RED:
                return ((self.canvas_red, 1, False),)
            else:
                return (self.canvas_red, 0, False), (self.canvas_black, 1, True)
        elif self.background == BLACK:
            if color == WHITE:
                return ((self.canvas_black, 1, False),)
            else:   # color == RED:
                return ((self.canvas_red, 1, False),)
        else:   # self.background == RED:
            ret = [(self.canvas_red, 0, True)]
            if color == BLACK:
                ret.append((self.canvas_black, 0, True))
            else:   # color == WHITE:
                ret.append((self.canvas_black, 1, False))
            return ret

    def tiny_text(self, string, x, y, color=BLACK):
        y = BOTTOM - y
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

    def line(self, x1, y1, x2, y2, color=BLACK):
        y1 = BOTTOM - y1
        y2 = BOTTOM - y2
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.line(x1, y1, x2, y2, color_value)

    def pixel(self, x, y, color=BLACK):
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.pixel(x, y, color_value)

    def hline(self, x, y, w, color=BLACK):
        y = BOTTOM - y
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.hline(x, y, w, color_value)

    def vline(self, x, y, h, color=BLACK):
        y = BOTTOM - y
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.vline(x, y, h, color_value)

    def rect(self, x, y, w, h, color=BLACK):
        y = BOTTOM - y
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.rect(x, y, w, h, color_value)

    def fill_rect(self, x, y, w, h, color=BLACK):
        y = BOTTOM - y
        for decided in self.color_decider(color):
            canvas, color_value, _ = decided
            canvas.fill_rect(x, y, w, h, color_value)

    def chart(self, values, maximum, minimum, color=BLACK):
        # val = 66
        # norm = (val - minimum)/(maximum - minimum)
        # out = norm*(top-bottom)+bottom
        # values = [int(out)]*100
        optimized_values = [int(((val - minimum) / (maximum - minimum)) * ((BOTTOM - TOP) + TOP)) for val in values]

        # self.eink.line(0, 0, w, 0, color)  # top horizontal
        # self.eink.line(0, h, w, h, color)  # bottom horizontal

        x = 0
        y = 0
        w = 249
        h = 121
        thickness = 3
        for thick in range(thickness):
            self.line(x+thick, y, x+thick, h, color)  # left vertical

        thickness = 1
        for thick in range(thickness):
            self.line(x, y+thick, w, y+thick, color)    # left vertical

        spread = 1
        for index, _ in enumerate(optimized_values, start=1):
            value = optimized_values[-index]
            y1 = value
            x1 = w - index*spread
            x2 = w - ((index*spread)+spread)
            try:
                value = optimized_values[-index - 1]
                y2 = value
            except IndexError:
                break

            # print("x1:", x1, " y1:", y1)
            # print("x2:", x2, " y2:", y2)
            thickness = 2
            for thick in range(thickness):
                self.line(x1, y1+thick, x2, y2+thick, RED)
        #
        # self.line(LEFT+4, TOP, LEFT+4, BOTTOM, color)  # left vertical
        # self.line(LEFT+5, TOP, LEFT+5, BOTTOM, color)  # left vertical
        #
        self.fill_rect(x+3, h, 20, 12, WHITE)
        self.tiny_text(str(maximum), x+5, h, color)
        self.fill_rect(x+3, y+32, 20, 12, WHITE)
        self.tiny_text(str(minimum), x+5, x+9, color)

        self.fill_rect(w-32, h, 33, 12, WHITE)
        self.tiny_text(str(values[-1]), w-31, h, RED)
