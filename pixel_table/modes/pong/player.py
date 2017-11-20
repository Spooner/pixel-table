from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.touch_button import TouchButton
from ...base_player import BasePlayer
from ...sprites.rectangle_sprite import RectangleSprite
from ...sprites.score import Score


class Player(BasePlayer):
    MOVE_SPEED = 10
    PUSH_SPEED = 4

    def __init__(self, index):
        if index == 0:
            x, y, width, height, self._move_left = 7, 14, 3, 1, (-1, 0)
        elif index == 1:
            x, y, width, height, self._move_left = 6, 1, 3, 1, (1, 0)
        elif index == 2:
            x, y, width, height, self._move_left = 1, 7, 1, 3, (0, -1)
        elif index == 3:
            x, y, width, height, self._move_left = 14, 6, 1, 3, (0, 1)
        else:
            raise ValueError

        super(Player, self).__init__(index, [TouchButton.LEFT, TouchButton.RIGHT])

        self._velocity_x = self._velocity_y = 0
        self._paddle = RectangleSprite(x=x, y=y, width=width, height=height, color=(1, 1, 1))
        self._score = Score(self._index, score=3)

    def on_touch_button_held(self, player_index, button_index, dt):
        if player_index != self._index:
            return

        distance = self.MOVE_SPEED * dt

        self._velocity_x = self._velocity_y = 0
        rect = (0, 0, 16, 16)
        previous_pos = self._paddle.int_position
        if button_index == TouchButton.LEFT:
            self._paddle.move_by(distance * self._move_left[0], distance * self._move_left[1], constrain=rect)
            if self._paddle.int_position != previous_pos:
                self._velocity_x = self.PUSH_SPEED * self._move_left[0]
                self._velocity_y = self.PUSH_SPEED * self._move_left[1]
        elif button_index == TouchButton.RIGHT:
            self._paddle.move_by(distance * -self._move_left[0], distance * -self._move_left[1], constrain=rect)
            if self._paddle.int_position != previous_pos:
                self._velocity_x = self.PUSH_SPEED * -self._move_left[0]
                self._velocity_y = self.PUSH_SPEED * -self._move_left[1]
        else:
            pass  # Ignore ACTION button

    @property
    def velocity_x(self):
        return self._velocity_x

    @property
    def velocity_y(self):
        return self._velocity_y

    @property
    def paddle(self):
        return self._paddle

    def lose_point(self):
        self._score.score -= 1

    def render(self, pixel_grid):
        super(Player, self).render(pixel_grid)
        self._paddle.render(pixel_grid)
        self._score.render(pixel_grid)
