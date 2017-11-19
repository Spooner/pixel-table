from __future__ import absolute_import, division, print_function, unicode_literals

import time

import numpy as np
from noise import snoise3

from ..mode import Mode


class Noise(Mode):
    class State(object):
        RED = "RED"
        GREEN = "GRN"
        BLUE = "BLUE"
        GREYSCALE = "GREY"
        FULL_COLOR = "RGB"

    NAME = "NOIS"
    STATES = [State.RED, State.GREEN, State.BLUE, State.GREYSCALE, State.FULL_COLOR]
    DEFAULT_STATE_INDEX = 0
    OCTAVES = 3
    PERSISTENCE = 0.5
    SCALE = 0.05
    TIME_SCALE = 0.5

    def __init__(self, index, state_index=None):
        super(Noise, self).__init__(index=index, state_index=state_index)
        self._cells = np.zeros((16, 16))

    def render(self, pixel_grid):
        t = time.clock() * self.TIME_SCALE
        state = self.state
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                rgb = self._rgb(state, x, y, t)
                pixel_grid.pixel(x, y).color = rgb

    def _noise(self, x, y, t):
        noise = snoise3(x * self.SCALE, y * self.SCALE, t, octaves=self.OCTAVES)
        return (noise + 1) / 2

    def _rgb(self, state, x, y, t):
        magnitude = self._noise(x, y, t)

        if state == self.State.RED:
            rgb = magnitude, 0, 0
        elif state == self.State.GREEN:
            rgb = 0, magnitude, 0
        elif state == self.State.BLUE:
            rgb = 0, 0, magnitude
        elif state == self.State.GREYSCALE:
            rgb = magnitude, magnitude, magnitude
        elif state == self.State.FULL_COLOR:
            rgb = magnitude, self._noise(x + 100, y + 100, t), self._noise(x + 200, y + 200, t)
        else:
            raise ValueError

        return rgb
