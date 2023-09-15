from lib.display.drawing_bw import Drawing, BLACK, WHITE
from lib.display.epd_2in13_bw import SEEN_WIDTH, SEEN_HEIGHT


class Widgets(Drawing):
    def __init__(self):
        super().__init__()

    def chart(self, values, maximum, minimum, color=BLACK):
        x = 0
        y = SEEN_WIDTH-1
        w = SEEN_HEIGHT-1
        h = 0

        optimized_values = [int(((val - minimum) / (maximum - minimum)) * ((y - h) + h)) for val in values]

        thickness = 3
        for thick in range(thickness):
            self.line(x+thick, y, x+thick, h, color)  # left vertical

        spread = 1
        for index, _ in enumerate(optimized_values, start=1):
            value = optimized_values[-index]
            y1 = y - value
            x1 = w - index*spread
            x2 = w - ((index*spread)+spread)
            try:
                value = optimized_values[-index - 1]
                y2 = y - value
            except IndexError:
                break

            thickness = 2
            for thick in range(thickness):
                self.line(x1, y1+thick, x2, y2+thick, color)

        self.fill_rect(x+3, h, 20, 12, WHITE)
        self.tiny_text(str(maximum), x+5, h, color)
        self.fill_rect(x+3, y-11, 20, 12, WHITE)
        self.tiny_text(str(minimum), x+5, y-8, color)

        self.fill_rect(w-32, h, 33, 12, WHITE)
        self.tiny_text(str(values[-1]), w-31, h, color)
