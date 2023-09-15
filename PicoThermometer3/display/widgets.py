from display.fundamentals_brw import Fundamentals, BLACK, WHITE, RED


class Widgets(Fundamentals):
    def __init__(self):
        super().__init__()

    def chart(self, values, maximum, minimum, color=BLACK):
        # val = 66
        # norm = (val - minimum)/(maximum - minimum)
        # out = norm*(top-bottom)+bottom
        # values = [int(out)]*100
        x = 0
        y = 121
        w = 249
        h = 0

        optimized_values = [int(((val - minimum) / (maximum - minimum)) * ((y - h) + h)) for val in values]

        # self.eink.line(0, 0, w, 0, color)  # top horizontal
        # self.eink.line(0, h, w, h, color)  # bottom horizontal


        thickness = 3
        for thick in range(thickness):
            self.line(x+thick, y, x+thick, h, color)  # left vertical

        # thickness = 1
        # for thick in range(thickness):
        #     self.line(x, y+thick, w, y+thick, color)

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
        self.fill_rect(x+3, y-11, 20, 12, WHITE)
        self.tiny_text(str(minimum), x+5, y-8, color)

        self.fill_rect(w-32, h, 33, 12, WHITE)
        self.tiny_text(str(values[-1]), w-31, h, RED)
