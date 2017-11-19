from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.rectangle_sprite import RectangleSprite


class Base(RectangleSprite):
    def __init__(self, x):
        super(Base, self).__init__(x=x, y=11, width=2, height=2, color=(1.0, 1.0, 0))
