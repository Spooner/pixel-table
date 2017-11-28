from __future__ import absolute_import, division, print_function, unicode_literals

class Console(object):
    def write_pixels(self, data):
        lines = []
        lines.append("===       Apotable %2dx%2d       ===" % (data.shape[0], data.shape[1]))
        lines.append("+" + "-" * (data.shape[0] * 2) + "+")

        for y in range(data.shape[1]):
            cells = []
            for x in range(data.shape[0]):
                color = self.rgb_to_terminal(*self.pixel(x, y).color)
                cells.append("\033[48;5;%sm  " % color)

            lines.append("|" + "".join(cells) + "\033[48;5;16m|")
        lines.append("+" + "-" * (self.data.shape[0] * 2) + "+")
        print(lines)
