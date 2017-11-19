from __future__ import absolute_import, division, print_function, unicode_literals

from ..mode import Mode


class Off(Mode):
    NAME = "OFF"
    STATES = [""]
    DEFAULT_STATE_INDEX = 0
