from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .player import Player
from .ball import Ball


class Pong(Mode):
    STATE_NAMES = ["players"]
    STATE_VALUES = [(2, ), (4, )]
    DEFAULT_STATE_INDEX = 0

    def __init__(self, index, state_index=None):
        super(Pong, self).__init__(index=index, state_index=state_index)
        self._players = list(Player(i) for i in range(self._get_state_value("players")))
        self._ball = Ball(list(p.paddle for p in self._players))

    def on_pre_render(self, pixel_grid):
        pixel_grid.clear()
