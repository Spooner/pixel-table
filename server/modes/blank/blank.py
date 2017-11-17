
from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode


class Blank(Mode):
    STATE_NAMES = [""]
    STATE_VALUES = [("creator:Bil Bas", ), ("live:16-Dec-17",)]
    DEFAULT_STATE_INDEX = 0
