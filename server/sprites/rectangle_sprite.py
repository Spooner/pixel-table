from __future__ import absolute_import, division, print_function, unicode_literals

from .sprite import Sprite


class RectangleSprite(Sprite):
    def on_render(self, pixel_grid):

        x, y = self.int_position
        for xx in range(x, x + self._width):
            for yy in range(y, y + self._height):
                pixel_grid.pixel(xx, yy).color = self._color
