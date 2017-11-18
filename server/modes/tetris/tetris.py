from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .player import Player


class Tetris(Mode):
    NAME = "TETR"
    STATES = [1, 2]
    DEFAULT_STATE_INDEX = 0

    def __init__(self, index, state_index=None):
        super(Tetris, self).__init__(index=index, state_index=state_index)
        self._players = list(Player(i, self.state) for i in range(self.state))

    def render(self, pixel_grid):
        pixel_grid.clear((0.1, 0.1, 0.1))
        for player in self._players:
            player.render(pixel_grid)

    def update(self, pixel_grid, dt):
        for player in self._players:
            player.update(pixel_grid, dt)

    @staticmethod
    def state_text(state):
        return str(state) + "P"
