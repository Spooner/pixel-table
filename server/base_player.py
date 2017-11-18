from __future__ import absolute_import, division, print_function, unicode_literals

from server.mixins.handles_events import HandlesEvents
from .sprites.touch_button import TouchButton


class BasePlayer(HandlesEvents):
    def __init__(self, index, buttons=None):
        super(BasePlayer, self).__init__()
        self._index = index
        self._buttons = [TouchButton(index, b) for b in (buttons or [])]
        self.initialize_event_handlers()

    def render(self, pixel_grid):
        for button in self._buttons:
            button.render(pixel_grid)
