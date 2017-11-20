from __future__ import absolute_import, division, print_function, unicode_literals

import smokesignal

from ..mode import Mode
from .player import Player
from .base import Base
from .saucer import Saucer
from .alien import Alien
from .bullet import Bullet

from ...sprites.rectangle_sprite import RectangleSprite


class Invaders(Mode):
    NAME = "INVA"
    STATES = [""]
    DEFAULT_STATE_INDEX = 0
    BASE_X = [1, 2, 5, 6, 9, 10, 13, 14]

    def __init__(self, index, state_index=None):
        super(Invaders, self).__init__(index=index, state_index=state_index)

        for x in self.BASE_X:
            Base.create(x, 12)
            Base.create(x, 13)

        for x in range(0, 11, 2):
            for y in range(1, 8, 2):
                Alien.create(x=x, y=y)

        self._player = Player(0)
        self._background = RectangleSprite(x=0, y=0, width=16, height=15, color=(0, 0, 0))
        self._game_over = False
        self._alien_direction = Alien.RIGHT

        self.spawn_saucer()

    def spawn_saucer(self):
        Saucer.create()

    def render(self, pixel_grid):
        pixel_grid.clear(color=(0.1, 0.1, 0.1))
        self._background.render(pixel_grid)

        super(Invaders, self).render(pixel_grid)

        if not self._game_over:
            self._player.render(pixel_grid)

    def update(self, pixel_grid, dt):
        if self._game_over:
            return

        super(Invaders, self).update(pixel_grid, dt)

        aliens = [o for o in self.objects if isinstance(o, Alien)]
        bullets = [o for o in self.objects if isinstance(o, Bullet)]
        targets = [o for o in self.objects if not isinstance(o, Bullet)]

        self._move_aliens(aliens, dt)
        self._collisions(bullets, targets)
        self._turn_at_edge(aliens)

    def _turn_at_edge(self, aliens):
        for alien in aliens:
            if not 0 <= alien.int_position[0] < 16:
                self._alien_direction = -self._alien_direction
                self.emit("alien_advance", self._alien_direction)
                break

    def _collisions(self, bullets, targets):
        for bullet in bullets:
            for target in targets:
                if target.collide_point(*bullet.int_position):
                    target.hit_by(bullet)
                    bullet.hit_by(target)
                    break

    def _move_aliens(self, aliens, dt):
        move_distance = (Alien.BASE_SPEED + (Alien.VARIABLE_SPEED * (24 - len(aliens)))) * dt * self._alien_direction
        for alien in aliens:
            alien.move_by(move_distance, 0)

    def on_game_over(self):
        self._game_over = True
        smokesignal.clear_all()
