from __future__ import absolute_import, division, print_function, unicode_literals

import random
import time

from server.sprites.rectangle_sprite import RectangleSprite


class Ball(RectangleSprite):
    INITIAL_SPEED = 10

    def __init__(self, players):
        super(Ball, self).__init__(x=7, y=7, width=1, height=1, color=(0.5, 1.0, 0.5))

        self._players = players
        self._vel_x = self._vel_y = 0
        self._reset(random.randrange(0, len(players)))
        self._wait_until = None

    def _reset(self, server_number, score=False):
        if score:
            self._players[server_number].lose_point()

        self._vel_x = 0
        if server_number == 0:
            self._vel_x, self._vel_y = 0, self.INITIAL_SPEED
            self._x, self._y = 7, 3
        elif server_number == 1:
            self._vel_x, self._vel_y = 0, -self.INITIAL_SPEED
            self._x, self._y = 8, 12
        elif server_number == 2:
            self._vel_x, self._vel_y = self.INITIAL_SPEED, 0
            self._x, self._y = 3, 8
        elif server_number == 3:
            self._vel_x, self._vel_y = -self.INITIAL_SPEED, 0
            self._x, self._y = 12, 7

        self._wait_until = time.clock() + 0.5

    def on_update(self, pixel_grid, dt):
        if self._wait_until:
            if time.clock() < self._wait_until:
                return
            else:
                self._wait_until = None

        self._x += self._vel_x * dt
        self._y += self._vel_y * dt

        x, y = self.int_position
        # Hit a side (either a point scored or a bounce, depending on number of players)
        if y < 0:
            self._reset(0, score=True)
        elif y > 15:
            self._reset(1, score=True)
        elif x < 0:
            if len(self._players) >= 3:
                self._reset(2, score=True)
            else:
                self._x = 0
                self._vel_x = -self._vel_x
        elif x > 15:
            if len(self._players) >= 4:
                self._reset(3, score=True)
            else:
                self._x = 15
                self._vel_x = -self._vel_x

        # Hit a paddle.
        for player in self._players:
            if player.paddle.collide_point(x, y):
                if self._vel_y > 0:
                    self._y = 13
                elif self._vel_y < 0:
                    self._y = 2
                # TODO bounce based on angle of incidence and/or where on the bat?
                self._vel_x, self._vel_y = -self._vel_x, -self._vel_y

