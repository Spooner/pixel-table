from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from ...sprites.sprite import Sprite


class Aliens(Sprite):
    SPEED = 1
    LEFT, RIGHT = -1, 1

    def __init__(self):
        width, height = 7 * 2 - 1, 4 * 2 - 1

        super(Aliens, self).__init__(x=0, y=2, width=width, height=height)

        self._cells = np.zeros((height, width))
        for x in range(0, self._cells.shape[1], 2):
            for y in range(0, self._cells.shape[0], 2):
                self._cells[y][x] = 1

        self._direction = 1

    def update(self, pixel_grid, dt):
        bounds = self._bounds()
        if bounds[1] + bounds[3] - 1 >= 14:
            return

        self.move_by(dt * self.SPEED * self._direction, 0)

        x, y = self.int_position
        bounds = self._bounds()

        if self._direction == self.LEFT and bounds[0] < 0:
            self.move_to(0, y + 1)
            self._direction = self.RIGHT
        elif self._direction == self.RIGHT and bounds[0] + bounds[2] - 1 > 15:
            self.move_to(bounds[0] - 1, y + 1)
            self._direction = self.LEFT

    def render(self, pixel_grid):
        pos = self.int_position
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                if cell == 1:
                    pixel_grid.pixel(pos[0] + x, pos[1] + y).color = (1, 1, 1)

    def _bounds(self):
        x_min = y_min = float("inf")
        x_max = y_max = -float("inf")

        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                if cell == 1:
                    x_min = min(x_min, x)
                    x_max = max(x_max, x)
                    y_min = min(y_min, y)
                    y_max = max(y_max, y)

        x_, y_ = self.int_position

        return x_ + x_min, y_ + y_min, x_max - x_min + 1, y_max - y_min + 1
