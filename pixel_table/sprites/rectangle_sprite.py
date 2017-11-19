from __future__ import absolute_import, division, print_function, unicode_literals

from .sprite import Sprite


class RectangleSprite(Sprite):
    def render(self, pixel_grid):
        x, y = self.int_position
        for xx in range(x, x + self._width):
            for yy in range(y, y + self._height):
                if 0 <= xx < 16 and 0 <= yy < 16:
                    pixel_grid.pixel(xx, yy).color = self.color
