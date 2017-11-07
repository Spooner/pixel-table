from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random

from .mode import Mode


class Drop(object):
    def __init__(self):
        self._x = self._y = self._length = self._speed = 0
        self.reset()

    def update(self, dt):
        self._y += self._speed * dt

        if self._y > 16 + self._length:
            self.reset()

    def reset(self, initial=True):
        self._x = random.randrange(0, 16)
        self._y = random.randrange(-20 if initial else -10, 0)
        self._length = random.randrange(5, 12)
        self._speed = random.randrange(4, 7)

    def tail(self):
        head_y = math.floor(self._y)

        for i in range(self._length):
            if i == 0:
                r = b = 0.5
            elif i == 1:
                r = b = 0.25
            else:
                r = b = 0

            y = head_y - i
            if 0 <= y <= 15:
                yield self._x, y, (r, 0.5, b)


class MatrixRain(Mode):
    VALUE_NAMES = ['num_drops']
    VALID_NUMBER_OF_DROPS = [1, 2, 4, 8, 16, 32, 64]
    DEFAULT_NUMBER_OF_DROPS = 16

    def __init__(self, pixel_grid, index):
        super(MatrixRain, self).__init__(pixel_grid, index)
        self._drops = []

    @property
    def num_drops(self):
        return len(self._drops)

    @num_drops.setter
    def num_drops(self, value):
        while self.num_drops < value:
            self._drops.append(Drop())

        self._drops = self._drops[:value]

    def on_activate(self):
        self.num_drops = self.DEFAULT_NUMBER_OF_DROPS

    def on_deactivate(self):
        self._drops = []

    def on_update(self, dt):
        # Fade all.
        self._pixel_grid.fade(0.2 * dt)

        # Move drops down a bit & restart any that have fallen off..
        for drop in self._drops:
            drop.update(dt)

            for x, y, color in drop.tail():
                pixel = self._pixel_grid.pixel(x, y)
                pixel.color = color

    def on_state_button_press(self):
        index = (self.VALID_NUMBER_OF_DROPS.index(self.num_drops) + 1) % len(self.VALID_NUMBER_OF_DROPS)
        self.num_drops = self.VALID_NUMBER_OF_DROPS[index]
