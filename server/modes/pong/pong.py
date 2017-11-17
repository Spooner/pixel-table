from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .player import Player
from .ball import Ball


class Pong(Mode):
    STATES = [2, 4]
    DEFAULT_STATE_INDEX = 0

    def __init__(self, index, state_index=None):
        super(Pong, self).__init__(index=index, state_index=state_index)
        self._players = list(Player(i) for i in range(self.state))
        self._ball = Ball(self._players)

    def on_pre_render(self, pixel_grid):
        pixel_grid.clear()

    @staticmethod
    def state_text(state):
        return str(state) + "P"
