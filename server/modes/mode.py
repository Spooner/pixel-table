from __future__ import absolute_import, division, print_function, unicode_literals

import re

from server.mixins.handles_events import HandlesEvents


class Mode(HandlesEvents):
    VALUE_NAMES = []

    def __init__(self, index):
        super(Mode, self).__init__()
        self._index = index
        self.initialize_event_handlers()

    @property
    def index(self):
        return self._index

    def dump(self, lines):
        mode = re.sub(r"([A-Z])", lambda m: " " + m.group(1), type(self).__name__).strip()
        line1 = "%02d) %s" % (self._index + 1, mode)

        names = (n.replace("num_", "").replace("_", " ") for n in self.VALUE_NAMES)
        values = (getattr(self, n) for n in self.VALUE_NAMES)
        line2 = "; ".join("%s=%s" % nv for nv in zip(names, values))

        lines.append("  /1\\ /2\\  |%-16s|     " % line1[:16])
        lines.append("  \\_/ \\_/  |%-16s|     " % line2[:16])
