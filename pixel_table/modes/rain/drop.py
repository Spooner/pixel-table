from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random

from ...sprites.sprite import Sprite


class Drop(Sprite):
    def __init__(self):
        super(Drop, self).__init__(0, 0)
        self._length = self._speed = 0
        self.reset()
        self.initialize_event_handlers()

    def update(self, pixel_grid, dt):
        self._y += self._speed * dt

        if self._y > 16 + self._length:
            self.reset()

    def render(self, pixel_grid):
        for x, y, color in self.tail():
            pixel = pixel_grid.pixel(x, y)
            pixel.color = color

    def reset(self, initial=True):
        self._x = random.randrange(0, 16)
        self._y = random.randrange(-20 if initial else -10, 0)
        self._length = random.randrange(5, 12)
        self._speed = random.randrange(2, 4)

    def tail(self):
        head_y = math.floor(self._y)

        for i in range(self._length):
            if i == 0:
                r = b = 0.5
            elif i == 1:
                r = b = 0.25
            else:
                r = b = 0

            y = head_y - i
            if 0 <= y <= 15:
                yield self._x, y, (r, 0.5, b)
