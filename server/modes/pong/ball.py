from __future__ import absolute_import, division, print_function, unicode_literals

import random

from server.sprites.rectangle_sprite import RectangleSprite


class Ball(RectangleSprite):
    INITIAL_SPEED = 10

    def __init__(self, paddles):
        super(Ball, self).__init__(x=7, y=7, width=1, height=1)

        self._paddles = paddles
        self._vel_x = self._vel_y = 0
        self._reset(random.randrange(0, len(self._paddles)))

    def _reset(self, server_number):
        self._vel_x = 0
        if server_number == 0:
            self._vel_y = self.INITIAL_SPEED
            self._x, self._y = 7, 3
        else:
            self._vel_y = -self.INITIAL_SPEED
            self._x, self._y = 8, 12

    def on_update(self, pixel_grid, dt):
        self._x += self._vel_x * dt
        self._y += self._vel_y * dt

        x, y = self.int_position

        # Hit ends.
        if y < 0:
            self._reset(0)
        elif y > 15:
            self._reset(1)

        # Hit sides.
        if x > 15:
            self._x = 15
            self._vel_x = -self._vel_x
        elif x < 0:
            self._x = 0
            self._vel_x = -self._vel_x

        # Hit a paddle.
        for paddle in self._paddles:
            if paddle.collide_point(x, y):
                if self._vel_y > 0:
                    self._y = 13
                elif self._vel_y < 0:
                    self._y = 2
                # TODO bounce based on angle of incidence and/or where on the bat?
                self._vel_x, self._vel_y = -self._vel_x, -self._vel_y

