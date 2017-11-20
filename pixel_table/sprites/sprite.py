from __future__ import absolute_import, division, print_function, unicode_literals

from ..mixins.handles_events import HandlesEvents


class Sprite(HandlesEvents):
    def __init__(self, x, y, width=1, height=1, color=(1.0, 1.0, 1.0)):
        self._x, self._y = x, y
        self._width, self._height = width, height
        self._color = color
        self._is_destroyed = False
        self.initialize_event_handlers()

    @property
    def int_position(self):
        return int(round(self._x)), int(round(self._y))

    def collide_point(self, x, y):
        display_x, display_y = self.int_position
        return (display_x <= x < display_x + self._width) and (display_y <= y < display_y + self._height)

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

    def move_by(self, dx, dy, constrain=None):
        self._x += dx
        self._y += dy

        if constrain is not None:
            self._constrain(constrain)

    def move_to(self, dx, dy, constrain=None):
        self._x = dx
        self._y = dy

        if constrain is not None:
            self._constrain(constrain)

    def _constrain(self, rect):
        """Constrain the position of the sprite within a rectangular area
        @param rect tuple (x, y, width, height)
        """
        self._x = min(max(self._x, rect[0]), rect[2] - self._width)
        self._y = min(max(self._y, rect[1]), rect[3] - self._height)

    @property
    def color(self):
        return self._color

    @property
    def rect(self):
        x, y = self.int_position
        return x, y, self._width, self._height

    def render(self, pixel_grid):
        pass

    def update(self, pixel_grid, dt):
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        cls.emit("create_object", obj)
        return obj

    def destroy(self):
        if not self._is_destroyed:
            self._is_destroyed = True
            self.emit("destroy_object", self)

    def __str__(self):
        x, y = self.int_position
        return "<{} ({}, {}) {}x{} {}>".format(type(self).__name__, x, y, self.width, self.height, self.color)