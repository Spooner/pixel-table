from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.rectangle_sprite import RectangleSprite


class Bullet(RectangleSprite):
    SPEED = 20

    def __init__(self, x, y, direction):
        super(Bullet, self).__init__(x=x, y=y, width=1, height=1, color=(1.0, 1.0, 1.0))
        self._direction = direction

    def update(self, pixel_grid, dt):
        self.move_by(0, dt * self.SPEED * self._direction)
