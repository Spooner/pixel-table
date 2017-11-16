from __future__ import absolute_import, division, print_function, unicode_literals

from server.mixins.handles_events import HandlesEvents


class Sprite(HandlesEvents):
    def __init__(self, x, y, width=1, height=1, color=(1, 1, 1)):
        self._x, self._y = x, y
        self._width, self._height = width, height
        self._color = color
        self.initialize_event_handlers()

    @property
    def int_position(self):
        return int(round(self._x)), int(round(self._y))

    def collide_point(self, x, y):
        return (self._x <= x < self._x + self._width) and (self._y <= y < self._y + self._height)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def move_by(self, dx, dy, constrain=False):
        self._x += dx
        self._y += dy
        if constrain:
            self._constrain()

    def move_to(self, dx, dy, constrain=False):
        self._x = dx
        self._y = dy
        if constrain:
            self._constrain()

    def _constrain(self):
        self._x = min(max(self._x, 0), 16 - self._width)
        self._y = min(max(self._x, 0), 16 - self._height)

    def _render(self, pixel_grid):
        pass
