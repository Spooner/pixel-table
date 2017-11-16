from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .drop import Drop


class MatrixRain(Mode):
    VALUE_NAMES = ['num_drops']
    VALID_NUMBER_OF_DROPS = [1, 2, 4, 8, 16, 32, 64]
    DEFAULT_NUMBER_OF_DROPS = 16

    def __init__(self, index):
        super(MatrixRain, self).__init__(index)
        self._drops = []
        self._next_fade = None
        self.num_drops = self.DEFAULT_NUMBER_OF_DROPS

    @property
    def num_drops(self):
        return len(self._drops)

    @num_drops.setter
    def num_drops(self, value):
        while self.num_drops < value:
            self._drops.append(Drop())

        self._drops = self._drops[:value]

    def on_update(self, pixel_grid, dt):
        self._next_fade = 0.2 * dt

    def on_pre_render(self, pixel_grid):
        pixel_grid.fade(self._next_fade)

    def on_state_button_press(self):
        index = (self.VALID_NUMBER_OF_DROPS.index(self.num_drops) + 1) % len(self.VALID_NUMBER_OF_DROPS)
        self.num_drops = self.VALID_NUMBER_OF_DROPS[index]
