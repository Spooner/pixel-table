from __future__ import absolute_import, division, print_function, unicode_literals

import re


class Mode(object):
    VALUE_NAMES = []

    def __init__(self, pixel_grid):
        self._pixel_grid = pixel_grid

    def on_update(self, dt):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_button_press(self, x, y):
        pass

    def on_state_button(self):
        pass

    def dump(self):
        line1 = "12 " + re.sub(r"([A-Z])", lambda m: " " + m.group(1), type(self).__name__).strip()

        names = (n.replace("num_", "#").replace("_", " ") for n in self.VALUE_NAMES)
        values = (getattr(self, n) for n in self.VALUE_NAMES)
        line2 = "; ".join("%s=%s" % nv for nv in zip(names, values))

        print("|%-16s|" % line1[:16])
        print("|%-16s|" % line2[:16])
