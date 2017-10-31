from __future__ import absolute_import, division, print_function, unicode_literals

import re


class Mode(object):
    STATE_NAME = None

    def __init__(self, pixel_grid):
        self._pixel_grid = pixel_grid

    def on_update(self, dt):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_pixel_press(self, x, y):
        pass

    def on_state_button(self):
        pass

    def dump(self):
        print()
        print("Mode: %s" % re.sub(r"([A-Z])", lambda m: " " + m.group(1), type(self).__name__).strip())
        print("%s: %s" % (self.STATE_NAME.replace("_", " ").capitalize(), getattr(self, self.STATE_NAME)))
        print()
