from __future__ import absolute_import, division, print_function, unicode_literals

import math

from ...sprites.rectangle_sprite import RectangleSprite
from .bullet import Bullet


class Alien(RectangleSprite):
    BASE_SPEED = 0.5
    VARIABLE_SPEED = 0.1  # Additional speed per dead alien.
    LEFT, RIGHT = -1, 1

    def __init__(self, x, y):
        super(Alien, self).__init__(x=x, y=y, width=1, height=1, color=(1, 1, 1))

    def hit_by(self, other):
        if isinstance(other, Bullet) and other.is_alien:
            return

        self.destroy()

    def on_alien_advance(self, direction):
        self.move_by(0, 1)

        if direction == self.LEFT:
            self._x = math.floor(self._x)
        else:
            self._x = math.ceil(self._x)

        y = self.int_position[1]
        if 12 <= y <= 13:
            self.emit("destroy_base", y)
        elif y >= 14:
            self.emit("game_over")
