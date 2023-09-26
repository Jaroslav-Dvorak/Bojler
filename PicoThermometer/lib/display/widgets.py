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

        self.fill_rect(x+3, h, 20, 12, WHITE)
        self.tiny_text(str(maximum), x+5, h, color)
        self.fill_rect(x+3, y-11, 20, 12, WHITE)
        self.tiny_text(str(minimum), x+5, y-8, color)

        spread = 1
        for index, _ in enumerate(optimized_values, start=1):
            try:
                value = optimized_values[-index]
            except IndexError:
                return
            y1 = y - value
            x1 = w - index*spread
            x2 = w - ((index*spread)+spread)
            try:
                value = optimized_values[-index - 1]
                y2 = y - value
            except IndexError:
                pass
            else:
                thickness = 2
                for thick in range(thickness):
                    self.line(x1, y1+thick, x2, y2+thick, color)

        self.fill_rect(w-32, h, 33, 12, WHITE)
        self.tiny_text(str(values[-1]), w-31, h, color)

    def battery_indicator(self, soc, x, y, color=BLACK):
        w = 40
        h = 15
        self.rect(x, y, w, h, color)
        self.fill_rect(x-4, y+4, 3, 7, color)

        soc = int(w / 100 * soc)
        soc_x = w - soc + x

        self.fill_rect(soc_x, y, soc, h, color)

    def qr_code(self, content, x, y, scale):
        from lib.display.uQR import QRCode
        qr = QRCode(border=0, box_size=10)
        qr.add_data(content)
        matrix = qr.get_matrix()
        for y_mat in range(len(matrix) * scale):                            # Scaling the bitmap by 2
            for x_mat in range(len(matrix[0]) * scale):                     # because my screen is tiny.
                value = not matrix[int(y_mat / scale)][int(x_mat / scale)]  # Inverting the values because
                self.pixel(x_mat+x, y_mat+y, value)

    def wifi_indicator(self, x, y, strength, color=BLACK):
        self.fill_circle(x, y, 30, color=color)
