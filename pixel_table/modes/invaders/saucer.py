from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.rectangle_sprite import RectangleSprite


class Saucer(RectangleSprite):
    SPEED = 3

    def __init__(self, direction):
        super(Saucer, self).__init__(x=0 if direction > 0 else 14, y=1, width=2, height=1, color=(1, 0, 0))
        self._direction = direction

    def update(self, pixel_grid, dt):
        self.move_by(dt * self.SPEED * self._direction, 0)
