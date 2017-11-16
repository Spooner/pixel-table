from __future__ import absolute_import, division, print_function, unicode_literals


class Pixel(object):
    def __init__(self, x, y, pixel_grid):
        self._x, self._y = x, y
        self._pixel_grid = pixel_grid
        self._character = " "

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def position(self):
        return self._x, self._y

    @property
    def color(self):
        return self._pixel_grid.get_color(self._x, self._y)

    @color.setter
    def color(self, color):
        self._pixel_grid.set_color(self._x, self._y, color)

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, value):
        assert isinstance(value, (str, unicode)) and len(value) == 1
        self._character = value

    def __str__(self):
        return "<Pixel ({x}, {y}) {color} '{char}'>".format(x=self._x, y=self._y,
                                                            color=self.color,
                                                            char=self._character)
