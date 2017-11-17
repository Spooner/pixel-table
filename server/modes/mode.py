from __future__ import absolute_import, division, print_function, unicode_literals

import re

from server.mixins.handles_events import HandlesEvents


class Mode(HandlesEvents):
    STATE_NAMES = None
    STATE_VALUES = None
    DEFAULT_STATE_INDEX = None

    def __init__(self, index, state_index=None):
        super(Mode, self).__init__()
        self._index = index
        self._state_index = self.DEFAULT_STATE_INDEX if state_index is None else state_index % len(self.STATE_VALUES)
        self.initialize_event_handlers()

    @property
    def index(self):
        return self._index

    @property
    def state_index(self):
        return self._state_index

    def dump(self, lines):
        mode = re.sub(r"([A-Z])", lambda m: " " + m.group(1), type(self).__name__).strip()
        lines.append(" /1\\                       WER  ")

        line1 = "%02d) %s" % (self._index, mode)
        lines.append(" \\_/  |%-16s|  Q   T " % line1[:16])

        line2 = "; ".join("%s=%s" % nv for nv in zip(self.STATE_NAMES, self.STATE_VALUES[self._state_index]))
        lines.append(" /2\\  |%-16s|  A   G " % line2[:16])

        lines.append(" \\_/                      Z   B ")
        lines.append("                           XCV  ")

    def _get_state_value(self, name):
        return self.STATE_VALUES[self._state_index][self.STATE_NAMES.index(name)]
