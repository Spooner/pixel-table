# https://fontstruct.com/fontstructions/show/716744/3_by_5_pixel_font
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from PIL import Image

from .sprite import Sprite


class Text(Sprite):
    CHARACTERS = {
        (3, 5): "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,""''"'?!@_                                 ',
    }

    _all_coords = {}

    def __init__(self, x, y, text, size=(3, 5), color=(1, 1, 1), spacing=1):
        self._coords = []
        char_width = size[0] + spacing
        self._calculate_coords(size, text, char_width)
        super(Text, self).__init__(x=x, y=y, width=len(text) * char_width, height=5, color=color)

    def _calculate_coords(self, size, text, char_width):
        for i, char in enumerate(text):
            for x, y in self._char_coords(size, char):
                self._coords.append((x + (i * char_width), y))

    def _char_coords(self, size, char):
        if size not in self._all_coords:
            self._all_coords[size] = self._load_coords_from_image(size)

        return self._all_coords[size][char]

    def _load_coords_from_image(self, size):
        coords = {}
        image = Image.open(os.path.join(os.path.dirname(__file__), "fonts", "%dx%d.png" % size))
        for i, char in enumerate(self.CHARACTERS[size]):
            x_offset = i * (size[0] + 1)
            char_coords = []
            for x in range(0, size[0]):
                for y in range(0, size[1]):
                    a = image.getpixel((x + x_offset, y))[3]
                    if a >= 128:
                        char_coords.append((x, y))

            coords[char] = char_coords

        return coords

    def render(self, pixel_grid):
        base_x, base_y = self.int_position
        for offset_x, offset_y in self._coords:
            screen_x, screen_y = base_x + offset_x, base_y + offset_y
            if 0 <= screen_x < 16 and 0 <= screen_y < 16:
                pixel_grid.pixel(screen_x, screen_y).color = self.color
