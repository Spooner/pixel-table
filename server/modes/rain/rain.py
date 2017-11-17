from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .drop import Drop


class Rain(Mode):
    STATES = [1, 2, 4, 8, 16, 32, 64]
    DEFAULT_STATE_INDEX = 3

    FADE = 0.2

    def __init__(self, index, state_index=None):
        super(Rain, self).__init__(index=index, state_index=state_index)
        self._drops = list(Drop() for _ in range(self.state))
        self._next_fade = None

    @property
    def num_drops(self):
        return len(self._drops)

    def on_update(self, pixel_grid, dt):
        self._next_fade = self.FADE * dt

    def on_pre_render(self, pixel_grid):
        if self._next_fade is not None:
            pixel_grid.fade(self._next_fade)

    @staticmethod
    def state_text(state):
        return "x" + str(state)
