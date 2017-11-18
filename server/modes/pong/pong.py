from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .player import Player
from .ball import Ball
from ...sprites.rectangle_sprite import RectangleSprite


class Pong(Mode):
    NAME = "PONG"
    STATES = [2, 4]
    DEFAULT_STATE_INDEX = 0

    def __init__(self, index, state_index=None):
        super(Pong, self).__init__(index=index, state_index=state_index)
        self._players = list(Player(i) for i in range(self.state))
        self._ball = Ball(self._players)

        if self.state == 2:
            x, y, width, height = 0, 1, 16, 14
        else:
            x, y, width, height = 1, 1, 14, 14

        self._background = RectangleSprite(x=x, y=y, width=width, height=height, color=(0, 0, 0))

    def update(self, pixel_grid, dt):
        self._ball.update(pixel_grid, dt)

    def render(self, pixel_grid):
        pixel_grid.clear((0.1, 0.1, 0.1))
        self._background.render(pixel_grid)
        for player in self._players:
            player.render(pixel_grid)
        self._ball.render(pixel_grid)

    @staticmethod
    def state_text(state):
        return str(state) + "P"
