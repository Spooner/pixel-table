from __future__ import absolute_import, division, print_function, unicode_literals

from ..mode import Mode
from ...sprites.text import Text


class Msg(Mode):
    STATES = [1, 2, 3, 4]
    DEFAULT_STATE_INDEX = 0
    SPEED = 8
    MESSAGES = "0123456789", "ABC,DEF,GHI.J", "abcdefghij", "A1B2C3D4E5"

    def __init__(self, index, state_index=None):
        super(Msg, self).__init__(index=index, state_index=state_index)
        self._text = Text(x=15, y=5, text=self.MESSAGES[self.state - 1])

    def on_pre_render(self, pixel_grid):
        pixel_grid.clear()

    def on_update(self, pixel_grid, dt):
        self._text.move_by(dt * -self.SPEED, 0)
        if self._text.x + self._text.width < 0:
            self._text.move_to(15, 5)
