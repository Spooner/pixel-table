from __future__ import absolute_import, division, print_function, unicode_literals

from server.mixins.handles_events import HandlesEvents

from .rectangle_sprite import RectangleSprite


class Score(RectangleSprite):
    CONFIG = {
        0: {"kwargs": {"x": 0, "y": 0, "width": 0, "height": 1}, "is_vertical": False, "is_inverted": False},
        1: {"kwargs": {"x": 15, "y": 15, "width": 0, "height": 1}, "is_vertical": False, "is_inverted": True},
        2: {"kwargs": {"x": 0, "y": 15, "width": 1, "height": 0}, "is_vertical": True, "is_inverted": False},
        3: {"kwargs": {"x": 15, "y": 0, "width": 1, "height": 0}, "is_vertical": True, "is_inverted": True},
    }

    def __init__(self, player_index, score=0):
        config = self.CONFIG[player_index]
        self._is_vertical = config["is_vertical"]
        self._is_inverted = config["is_inverted"]
        super(Score, self).__init__(color=(0.25, 0.50, 0.25), **config["kwargs"])
        self.score = score

    @property
    def score(self):
        if self._is_vertical:
            return self.height
        else:
            return self.width

    @score.setter
    def score(self, value):
        if self._is_vertical:
            self._height = value
            if self._is_inverted:
                self._y = 16 - value
        else:
            self._width = value
            if self._is_inverted:
                self._x = 16 - value


