from __future__ import absolute_import, division, print_function, unicode_literals

import smokesignal

from ...sprites.score import Score
from ...sprites.touch_button import TouchButton
from ...base_player import BasePlayer
from ...sprites.rectangle_sprite import RectangleSprite
from .bullet import Bullet


class Player(BasePlayer):
    MOVE_SPEED = 10

    def __init__(self, index):
        super(Player, self).__init__(index, [TouchButton.LEFT, TouchButton.RIGHT, TouchButton.ACTION])
        self._ship = RectangleSprite.create(x=5, y=14, width=1, height=1, color=(0, 1, 0))
        self._lives = Score.create(1, score=3)
        self._bullet = None

    def on_touch_button_held(self, player_index, button_index, dt):
        if player_index != self._index:
            return

        distance = self.MOVE_SPEED * dt
        rect = (0, 0, 16, 16)
        if button_index == TouchButton.LEFT:
            self._ship.move_by(-distance, 0, constrain=rect)
        elif button_index == TouchButton.RIGHT:
            self._ship.move_by(distance, 0, constrain=rect)
        elif button_index == TouchButton.ACTION and self._bullet is None:
            position = self._ship.int_position
            self._bullet = Bullet.create(x=position[0], y=position[1], direction=-1)

    def on_destroy_object(self, obj):
        if obj == self._bullet:
            self._bullet = None

    def on_game_over(self):
        self._ship.destroy()
        self._lives.destroy()

    def hit_by(self, other):
        self._lives.value -= 1
        if self._lives.value == 0:
            smokesignal.emit("game_over")
