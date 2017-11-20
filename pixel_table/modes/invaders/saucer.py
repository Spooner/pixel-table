from __future__ import absolute_import, division, print_function, unicode_literals

import random

from ...sprites.rectangle_sprite import RectangleSprite


class Saucer(RectangleSprite):
    SPEED = 3

    def __init__(self):
        direction = -1 if random.random() < 0.5 else +1
        super(Saucer, self).__init__(x=0 if direction > 0 else 14, y=0, width=2, height=1, color=(1, 0, 0))
        self._direction = direction

    def update(self, pixel_grid, dt):
        self.move_by(dt * self.SPEED * self._direction, 0)

    def hit_by(self, other):
        self.destroy()
