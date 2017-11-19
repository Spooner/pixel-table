from __future__ import absolute_import, division, print_function, unicode_literals

import random

from ...sprites.touch_button import TouchButton
from ...base_player import BasePlayer
from ...sprites.sprite_sheet import SpriteSheet
from ...sprites.rectangle_sprite import RectangleSprite


class Player(BasePlayer):
    SHAPES = "IJLOSTZ"
    HORIZONTAL_SPEED = 5
    DROP_SPEED = 2

    def __init__(self, index, num_players):
        super(Player, self).__init__(index, [TouchButton.LEFT, TouchButton.CENTER, TouchButton.RIGHT])

        if index == 0:
            color = (0, 0, 0)
            x = 0
            if num_players == 1:
                y, width, height = 0, 10, 15
            else:
                y, width, height = 1, 8, 14
        elif index == 1:
            color = (1 / 24, 1 / 24, 1 / 24)
            x, y, width, height = 8, 1, 8, 14
        else:
            raise ValueError

        self._index, self._num_players = index, num_players
        self._channel = RectangleSprite(x=x, y=y, width=width, height=height, color=color)
        self._shape = self._next_shape = None

        if num_players == 1:
            self._next_shape = self._random_shape(11, 4)
        self._create_shape()

    def _create_shape(self):
        if self._num_players == 2:
            self._shape = self._random_shape(3 if self._index == 0 else 11, 1 if self._index == 0 else 13)
        else:
            self._shape = self._random_shape(3, 0)
            self._next_shape = self._random_shape(11, 4)

    def _random_shape(self, x, y):
        return SpriteSheet(x=x, y=y, name="tetr/%s" % random.choice(self.SHAPES))

    def on_touch_button_held(self, player_index, button_index, dt):
        if player_index != self._index:
            return

        distance = self.HORIZONTAL_SPEED * dt
        if button_index == TouchButton.LEFT:
            self._shape.move_by(-distance if self._index == 0 else distance, 0, constrain=self._channel.rect)
        elif button_index == TouchButton.CENTER:
            pass  # TODO: Rotate.
        elif button_index == TouchButton.RIGHT:
            self._shape.move_by(distance if self._index == 0 else -distance, 0, constrain=self._channel.rect)

    def render(self, pixel_grid):
        super(Player, self).render(pixel_grid)
        self._channel.render(pixel_grid)
        self._shape.render(pixel_grid)
        if self._next_shape is not None:
            self._next_shape.render(pixel_grid)

    def update(self, pixel_grid, dt):
        distance = self.DROP_SPEED * dt
        self._shape.move_by(0, distance if self._index == 0 else -distance)
