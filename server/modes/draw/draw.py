from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode


class Paint(Mode):
    VALUE_NAMES = ["color"]

    def __init__(self, index):
        super(Paint, self).__init__(index)

        self._data = None
        self._color = (255, 255, 255)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
