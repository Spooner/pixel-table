from __future__ import absolute_import, division, print_function, unicode_literals

import smokesignal

from ...sprites.rectangle_sprite import RectangleSprite


class Base(RectangleSprite):
    INITIAL_HEALTH = 3
    COLORS = {
        1: (0.25, 0.25, 0),
        2: (0.5, 0.5, 0),
        3: (0.75, 0.75, 0),
    }

    def __init__(self, x, y):
        super(Base, self).__init__(x=x, y=y, width=1, height=1, color=(1.0, 1.0, 0))
        self._health = self.INITIAL_HEALTH

    def hit_by(self, obj):
        self._health -= 1
        if self._health == 0:
            self.destroy()

    @property
    def color(self):
        return self.COLORS[self._health]

    def on_destroy_base(self, y):
        if self.int_position[1] == y:
            self.destroy()
