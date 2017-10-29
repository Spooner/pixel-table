from __future__ import absolute_import, division, print_function, unicode_literals


class Mode(object):
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
