from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.score import Score
from ...sprites.touch_button import TouchButton
from ...base_player import BasePlayer
from ...sprites.rectangle_sprite import RectangleSprite
from .bullet import Bullet


class Player(BasePlayer):
    MOVE_SPEED = 10

    def __init__(self, index):
        super(Player, self).__init__(index, [TouchButton.LEFT, TouchButton.RIGHT, TouchButton.ACTION])
        self._ship = RectangleSprite(x=5, y=14, width=1, height=1, color=(0, 1, 0))
        self._lives = Score(0, 15, value=3)
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
            x, y = self._ship.int_position
            self._bullet = Bullet.create(x=x, y=y, is_alien=False)

    def on_destroy_object(self, obj):
        if obj == self._bullet:
            self._bullet = None

    def hit_by(self, other):
        self._lives.value -= 1
        if self._lives.value == 0:
            self.emit("game_over")

    def render(self, pixel_grid):
        super(Player, self).render(pixel_grid)
        self._lives.render(pixel_grid)
        self._ship.render(pixel_grid)
