from __future__ import absolute_import, division, print_function, unicode_literals

from ..mixins.handles_events import HandlesEvents


class Mode(HandlesEvents):
    NAME = None
    STATES = None
    DEFAULT_STATE_INDEX = 0

    def __init__(self, index, state_index=DEFAULT_STATE_INDEX):
        super(Mode, self).__init__()
        self._index = index
        self._state_index = self.DEFAULT_STATE_INDEX if state_index is None else state_index % len(self.STATES)
        self.initialize_event_handlers()

    @property
    def index(self):
        return self._index

    @property
    def state_index(self):
        return self._state_index

    @property
    def state(self):
        return self.STATES[self._state_index]

    @staticmethod
    def state_text(state):
        return str(state)[:4]

    @classmethod
    def state_line(cls, state):
        state_text = cls.state_text(state)
        if len(state_text) in [1, 2]:
            state_text += " "
        return state_text

    @classmethod
    def title_page(cls, index, state_index):
        state_index = (state_index or cls.DEFAULT_STATE_INDEX) % len(cls.STATES)
        return [
            " %02d " % index,
            "%-4s" % cls.NAME,
            "%4s" % cls.state_line(cls.STATES[state_index]),
        ]

    def dump(self, lines):
        title_page = self.title_page(self.index, self.state_index)
        lines.append(" /1\\    |%s|     WER   " % title_page[0])
        lines.append(" \\_/    |%s|    Q   T  " % title_page[1])
        lines.append(" /2\\    |%s|    A   G  " % title_page[2])
        lines.append(" \\_/              Z   B ")
        lines.append("                   XCV ")

    @property
    def mode(self):
        return type(self)

    def update(self, pixel_grid, dt):
        pass

    def render(self, pixel_grid):
        pass
