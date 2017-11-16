from __future__ import absolute_import, division, print_function, unicode_literals

from server.sprites.touch_button import TouchButton
from server.base_player import BasePlayer
from .paddle import Paddle


class Player(BasePlayer):
    PADDLE_SPEED = 10

    def __init__(self, index):
        if index == 0:
            x, y, width, height, self._move_left = 6, 14, 4, 1, (-1, 0)
        elif index == 1:
            x, y, width, height, self._move_left = 6, 1, 4, 1, (1, 0)
        elif index == 2:
            x, y, width, height, self._move_left = 1, 6, 1, 4, (0, -1)
        elif index == 3:
            x, y, width, height, self._move_left = 14, 6, 1, 4, (0, 1)
        else:
            raise ValueError

        self._paddle = Paddle(x=x, y=y, width=width, height=height)

        super(Player, self).__init__(index, [TouchButton.LEFT, TouchButton.RIGHT])

        self.initialize_event_handlers()

    def on_touch_button_held(self, player_index, button_index, dt):
        if player_index != self._index:
            return

        distance = self.PADDLE_SPEED * dt

        if button_index == TouchButton.LEFT:
            self._paddle.move_by(distance * self._move_left[0], distance * self._move_left[1], constrain=True)
        elif button_index == TouchButton.RIGHT:
            self._paddle.move_by(distance * -self._move_left[0], distance * -self._move_left[1], constrain=True)
        else:
            pass  # Ignore center button

    @property
    def paddle(self):
        return self._paddle
