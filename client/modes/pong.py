import random

from .mode import Mode
from ..sprites.rectangle_sprite import RectangleSprite
from ..sprites.button import Button


class PongPlayer(RectangleSprite):
    SPEED = 10

    def __init__(self, y, left, right):
        super(PongPlayer, self).__init__(x=6, y=y, width=4, height=1)
        self._left, self._right = left, right

    def update(self, dt):
        pass

    def render(self, pixels):
        super(PongPlayer, self).render(pixels)
        self._left.render(pixels)
        self._right.render(pixels)

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def move_left(self, dt):
        if self._x > 0:
            self._x -= self.SPEED * dt

    def move_right(self, dt):
        if self._x < 16 - self._width:
            self._x += self.SPEED * dt


class PongBall(RectangleSprite):
    INITIAL_SPEED = 10

    def __init__(self, pixel_grid, players):
        super(PongBall, self).__init__(x=7, y=7, width=1, height=1)

        self._pixel_grid = pixel_grid
        self._players = players
        self._vel_x = self._vel_y = 0
        self._reset(random.randrange(0, len(self._players)))

    def _reset(self, server_number):
        self._vel_x = 0
        if server_number == 0:
            self._vel_y = self.INITIAL_SPEED
            self._x, self._y = 7, 3
        else:
            self._vel_y = -self.INITIAL_SPEED
            self._x, self._y = 8, 12

    def update(self, dt):
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
        for player in self._players:
            if player.collide_point(x, y):
                if self._vel_y > 0:
                    self._y = 13
                elif self._vel_y < 0:
                    self._y = 2
                # TODO bounce based on angle of incidence and/or where on the bat?
                self._vel_x, self._vel_y = -self._vel_x, -self._vel_y


class Pong(Mode):
    NAME = "Pong"

    def __init__(self, **kwargs):
        super(Pong, self).__init__(**kwargs)
        self._players = []
        self._ball = None

    def on_activated(self):
        self._players.append(PongPlayer(14, Button("bottom", 0), Button("bottom", 2)))
        self._players.append(PongPlayer(1, Button("top", 0), Button("top", 2)))
        self._ball = PongBall(self._pixel_grid, self._players)

    def on_deactivated(self):
        self._players = []
        self._ball = None

    def on_pixel_held(self, pixel, dt):
        x, y = pixel.position
        if self._players[0].left.collide_point(x, y):
            self._players[0].move_left(dt)
        elif self._players[0].right.collide_point(x, y):
            self._players[0].move_right(dt)
        elif self._players[1].left.collide_point(x, y):
            self._players[1].move_right(dt)
        elif self._players[1].right.collide_point(x, y):
            self._players[1].move_left(dt)

    def update(self, dt):
        self._ball.update(dt)
        for player in self._players:
            player.update(dt)

        self._pixel_grid.clear()
        self._ball.render(self._pixel_grid)
        for player in self._players:
            player.render(self._pixel_grid)
