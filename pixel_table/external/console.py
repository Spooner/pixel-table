from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from ..colortrans import rgb2short


class Console(object):
    def __init__(self):
        self._color_lookup = {}

    def write_pixels(self, data):
        lines = [
            "\033[0;0H"  # Cursor to 0, 0
            "===       Apotable %2dx%2d       ===" % (data.shape[0], data.shape[1]),
            "+" + "-" * (data.shape[0] * 2) + "+",
        ]

        for y in range(data.shape[0]):
            cells = []
            for x in range(data.shape[1]):
                color = self.rgb_to_terminal(*data[x][y])
                cells.append("\033[48;5;%sm  " % color)

            lines.append("|" + "".join(cells) + "\033[48;5;16m|")
        lines.append("+" + "-" * (data.shape[0] * 2) + "+")
        print("\n".join(lines), file=sys.stderr)

    def rgb_to_terminal(self, r, g, b):
        r, g, b = round(r, 2), round(g, 2), round(b, 2)
        if (r, g, b) not in self._color_lookup:
            self._color_lookup[r, g, b] = rgb2short(r, g, b)
        return self._color_lookup[r, g, b]