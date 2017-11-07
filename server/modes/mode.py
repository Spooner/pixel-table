from __future__ import absolute_import, division, print_function, unicode_literals

import re
import sys


class Mode(object):
    VALUE_NAMES = []

    def __init__(self, pixel_grid, index):
        self._pixel_grid = pixel_grid
        self._index = index

    @property
    def index(self):
        return self._index

    def on_update(self, dt):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_button_press(self, n):
        pass

    def on_state_button_press(self):
        pass

    def dump(self, lines):
        mode = re.sub(r"([A-Z])", lambda m: " " + m.group(1), type(self).__name__).strip()
        line1 = "%02d) %s" % (self._index + 1, mode)

        names = (n.replace("num_", "").replace("_", " ") for n in self.VALUE_NAMES)
        values = (getattr(self, n) for n in self.VALUE_NAMES)
        line2 = "; ".join("%s=%s" % nv for nv in zip(names, values))

        lines.append("    |%-16s| /1\\ /2\\" % line1[:16])
        lines.append("    |%-16s| \\_/ \\_/" % line2[:16])
