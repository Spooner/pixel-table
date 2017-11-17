from __future__ import absolute_import, division, print_function, unicode_literals

from ..mode import Mode


class Blank(Mode):
    STATE_NAMES = [""]
    STATE_VALUES = [("creator:Bil Bas", ), ("live:16-Dec-17",), ("thanks:Mark C", ), ("thanks:Paul&Sam", )]
    DEFAULT_STATE_INDEX = 0
