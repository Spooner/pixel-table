from __future__ import absolute_import, division, print_function, unicode_literals

from ...sprites.touch_button import TouchButton
from ...base_player import BasePlayer
from ...sprites.rectangle_sprite import RectangleSprite
from .bullet import Bullet


class Player(BasePlayer):
    MOVE_SPEED = 10

    def __init__(self, index):
        super(Player, self).__init__(index, [TouchButton.LEFT, TouchButton.CENTER, TouchButton.RIGHT])
        self._ship = RectangleSprite(x=5, y=14, width=1, height=1, color=(0, 1, 0))
        self._bullets = []

    def render(self, pixel_grid):
        super(Player, self).render(pixel_grid)
        self._ship.render(pixel_grid)
        for bullet in self._bullets:
            bullet.render(pixel_grid)

    def update(self, pixel_grid, dt):
        for bullet in self._bullets:
            bullet.update(pixel_grid, dt)

    def on_touch_button_held(self, player_index, button_index, dt):
        distance = self.MOVE_SPEED * dt
        rect = (0, 0, 16, 16)
        if button_index == TouchButton.LEFT:
            self._ship.move_by(-distance, 0, constrain=rect)
        elif button_index == TouchButton.RIGHT:
            self._ship.move_by(distance, 0, constrain=rect)
        elif button_index == TouchButton.CENTER:
            position = self._ship.int_position
            self._bullets.append(Bullet(x=position[0], y=position[1], direction=-1))
