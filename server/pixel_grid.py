from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

import numpy as np

from .colortrans import rgb2short
from .external import External
from .pixel import Pixel


class PixelGrid(object):
    WIDTH, HEIGHT = 16, 16

    def __init__(self):
        super(PixelGrid, self).__init__()
        self.data = np.zeros([self.WIDTH, self.HEIGHT, 3])
        self._cell_width = None

        self._pixels = OrderedDict()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self._pixels[x, y] = Pixel(x, y, pixel_grid=self)

        self._external = External()
        self._color_lookup = {}

    def rgb_to_terminal(self, rgb):
        if rgb not in self._color_lookup:
            self._color_lookup[rgb] = rgb2short(rgb)
        return self._color_lookup[rgb]
    
    @property
    def pixels(self):
        return self._pixels.values()

    def clear(self, color=(0, 0, 0)):
        for pixel in self.pixels:
            pixel.color = color
            pixel.character = " "

    def pixel(self, x, y):
        return self._pixels[x, y]

    def export_data(self):
        return self.data.copy()

    def import_data(self, data):
        self.data = data

    def get_color(self, x, y):
        return self.data[x][y]

    def set_color(self, x, y, color):
        self.data[x][y] = color

    def fade(self, amount):
        for pixel in self.pixels:
            r, g, b = pixel.color
            pixel.color = max(r - amount, 0), max(g - amount, 0), max(b - amount, 0)

    def write(self):
        self._external.write_pixels(self.data)

    def dump(self, lines):
        lines.append("===       Apotable %2dx%2d       ===" % (self.data.shape[0], self.data.shape[1]))
        lines.append("+" + "-" * (self.data.shape[0] * 2) + "+")

        for y in range(self.data.shape[1]):
            cells = []
            for x in range(self.data.shape[0]):
                pixel = self._pixels[x, y]
                color = self.rgb_to_terminal(tuple((pixel.color * 255).astype("int8")))
                cells.append("\033[48;5;{color}m{char}{char}".format(color=color, char=pixel.character))

            lines.append("|" + "".join(cells) + "\033[48;5;16m|")
        lines.append("+" + "-" * (self.data.shape[0] * 2) + "+")



