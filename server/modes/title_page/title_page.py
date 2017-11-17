from __future__ import absolute_import, division, print_function, unicode_literals

import time

from ..mode import Mode
from ...sprites.text import Text
from ...sprites.rectangle_sprite import RectangleSprite


class TitlePage(Mode):
    """Transition to a "real" mode"""
    STATES = list(range(100))
    SHOW_TIME = 1
    _title_page = None

    @classmethod
    def title_page(cls, index, state_index):
        return cls._title_page

    def __init__(self, app, mode, index, state_index):
        super(TitlePage, self).__init__(index=index, state_index=state_index)
        self._app = app
        self._mode = mode
        type(self)._title_page = title_page = mode.title_page(index, state_index)
        self._switch_at = time.time() + self.SHOW_TIME

        self._mode_indicator = RectangleSprite(x=0, y=1, height=2, width=self.index, color=(0.25, 0.25, 0.50))
        self._texts = [Text(x=0, y=i * 6 + 4, text=t) for i, t in enumerate(title_page[1:])]

    def on_update(self, pixel_grid, dt):
        if time.time() >= self._switch_at:
            self._app.set_mode(self.mode, self.state_index, transition=False)

    @property
    def mode(self):
        return self._mode
