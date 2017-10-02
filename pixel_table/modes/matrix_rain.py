import random
import math

from kivy.properties import ObjectProperty

from .mode import Mode


class Drop:
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
    NAME = "Matrix Rain"

    num_drops = ObjectProperty(None)
    _drops = []

    def on_activated(self):
        self._pixel_grid.clear()
        for i in range(self.num_drops.value):
            self.add_drop()

    def add_drop(self):
        self._drops.append(Drop())

    def on_deactivated(self):
        self._drops.clear()

    def update_num_drops(self, value):
        for i in range(len(self._drops), value):
            self.add_drop()
        self._drops = self._drops[:value]

    def update(self, dt):
        if dt > 0.2:  # Ignore long initial dt.
            return

        # Fade all.
        self._pixel_grid.fade(0.2 * dt)

        # Move drops down a bit & restart any that have fallen off..
        for drop in self._drops:
            drop.update(dt)

            for x, y, color in drop.tail():
                pixel = self._pixel_grid.pixel(x, y)
                pixel.color = color
