from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.rectangle_sprite import RectangleSprite
from .aliens import Aliens


class Bullet(RectangleSprite):
    SPEED = 20

    def __init__(self, x, y, direction):
        super(Bullet, self).__init__(x=x, y=y, width=1, height=1, color=(0.5, 0.5, 0.5))
        self._direction = direction

    def update(self, pixel_grid, dt):
        self.move_by(0, dt * self.SPEED * self._direction)

        if not 1 <= self.int_position[1] <= 14:
            self.destroy()

    def hit_by(self, other):
        if isinstance(other, Aliens) and self._direction > 0:
            return
        self.destroy()
