from __future__ import absolute_import, division, print_function, unicode_literals

from ..mode import Mode
from .player import Player
from .base import Base
from .saucer import Saucer
from .aliens import Aliens
from ...sprites.rectangle_sprite import RectangleSprite
from ...sprites.score import Score

class Invaders(Mode):
    NAME = "INVA"
    STATES = [1, 2]
    DEFAULT_STATE_INDEX = 0

    def __init__(self, index, state_index=None):
        super(Invaders, self).__init__(index=index, state_index=state_index)
        self._player = Player(0)
        self._bases = [Base(i) for i in range(1, 14, 4)]
        self._saucer = Saucer(direction=1)
        self._aliens = Aliens()
        self._background = RectangleSprite(x=0, y=1, width=16, height=14, color=(0, 0, 0))
        self._lives = Score(0, score=3)

    def render(self, pixel_grid):
        pixel_grid.clear((0.1, 0.1, 0.1))
        self._background.render(pixel_grid)
        self._lives.render(pixel_grid)

        self._player.render(pixel_grid)
        if self._saucer is not None:
            self._saucer.render(pixel_grid)
        self._aliens.render(pixel_grid)
        for base in self._bases:
            base.render(pixel_grid)

    def update(self, pixel_grid, dt):
        self._player.update(pixel_grid, dt)
        if self._saucer is not None:
            self._saucer.update(pixel_grid, dt)
        self._aliens.update(pixel_grid, dt)

    @staticmethod
    def state_text(state):
        return str(state) + "P"
