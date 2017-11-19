from __future__ import absolute_import, division, print_function, unicode_literals

import random

from ..mode import Mode


class GameOfLife(Mode):
    NAME = "LIFE"
    STATES = [24, 48]
    DEFAULT_STATE_INDEX = 0
    PERIOD = 0.5
    ADJACENT_CELLS = [
        (-1, +1), (+0, +1), (+1, +1),
        (-1, +0),           (+1, +0),
        (-1, -1), (+0, -1), (+1, -1),
    ]

    class State(object):
        DEAD = 0
        ALIVE = 1

    def __init__(self, index, state_index=None):
        super(GameOfLife, self).__init__(index=index, state_index=state_index)
        self._cells = None
        self._time_to_tick = self.PERIOD
        self._reset()

    def _reset(self):
        self._cells = [[self.State.DEAD for _ in range(16)] for _ in range(16)]

        for _ in range(self.state):
            self._set_value(random.randrange(0, 16), random.randrange(0, 16), self.State.ALIVE)

    def render(self, pixel_grid):
        pixel_grid.clear()

        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                if cell is not self.State.DEAD:
                    pixel_grid.pixel(x, y).color = (1, 1, 1)

    def update(self, pixel_grid, dt):
        self._time_to_tick -= dt
        if self._time_to_tick <= 0:
            self._tick()
            self._time_to_tick += self.PERIOD

    def _tick(self):
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                neighbors = list(self._neighbors(x, y))
                if cell == self.State.DEAD:
                    if len(neighbors) == 3:
                        self._set_value(x, y, self.State.ALIVE)
                else:
                    if len(neighbors) not in [2, 3]:
                        self._set_value(x, y, self.State.DEAD)

    def _neighbors(self, x, y):
        for x_off, y_off in self.ADJACENT_CELLS:
            value = self._get_value(x + x_off, y + y_off)
            if value is not self.State.DEAD:
                yield value

    def _get_value(self, x, y):
        return self._cells[y % 16][x % 16]

    def _set_value(self, x, y, value):
        self._cells[y % 16][x % 16] = value




