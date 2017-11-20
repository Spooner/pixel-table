from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.rectangle_sprite import RectangleSprite


class Bullet(RectangleSprite):
    SPEED = 20

    def __init__(self, x, y, is_alien):
        super(Bullet, self).__init__(x=x, y=y, width=1, height=1, color=(0.5, 0.5, 0.5))
        self._is_alien = is_alien

    def update(self, pixel_grid, dt):
        self.move_by(0, dt * self.SPEED * self._direction)

        if not 0 <= self.int_position[1] <= 14:
            self.destroy()

    def hit_by(self, other):
        from .alien import Alien
        if isinstance(other, Alien) and self.is_alien:
            return
        self.destroy()

    @property
    def is_alien(self):
        return self._is_alien

    @property
    def _direction(self):
        return 1 if self.is_alien else -1
