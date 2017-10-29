from __future__ import absolute_import, division, print_function, unicode_literals

from .mode import Mode


class Paint(Mode):
    VALUES = ["color"]

    def __init__(self, pixel_grid):
        super(Paint, self).__init__(pixel_grid)

        self._data = None
        self._color = (255, 255, 255)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def on_activate(self):
        if self._data is not None:
            self._pixel_grid.import_data(self._data)

    def on_deactivate(self):
        self._data = self._pixel_grid.export_data()
