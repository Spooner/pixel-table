from __future__ import absolute_import, division, print_function, unicode_literals

from server.sprites.rectangle_sprite import RectangleSprite


class Paddle(RectangleSprite):
    def __init__(self, x, y, width, height):
        super(Paddle, self).__init__(x, y, width, height, color=(1, 1, 1))


