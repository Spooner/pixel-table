from __future__ import absolute_import, division, print_function, unicode_literals

from .rectangle_sprite import RectangleSprite


class Score(RectangleSprite):
    def __init__(self, x, y, is_vertical=False, is_inverted=False, value=0):
        self._is_vertical = is_vertical
        self._is_inverted = is_inverted

        if self._is_vertical:
            width, height = 1, value
        else:
            width, height = value, 1

        super(Score, self).__init__(x=x, y=y, width=width, height=height, color=(0.5, 0.5, 0.5))

    @property
    def value(self):
        if self._is_vertical:
            return self.height
        else:
            return self.width

    @value.setter
    def value(self, value):
        if self._is_vertical:
            self._height = value
            if self._is_inverted:
                self._y = 16 - value
        else:
            self._width = value
            if self._is_inverted:
                self._x = 16 - value


