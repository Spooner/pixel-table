from __future__ import absolute_import, division, print_function, unicode_literals

from .mode import Mode


class Pong(Mode):
    STATE_NAME = "num_players"
    VALID_NUM_PLAYERS = [2, 4]
    DEFAULT_NUM_PLAYERS = 2

    def __init__(self, pixel_grid):
        super(Pong, self).__init__(pixel_grid)

        self._num_players = self.DEFAULT_NUM_PLAYERS

    @property
    def num_players(self):
        return self._num_players

    @num_players.setter
    def num_players(self, value):
        assert value in self.VALID_NUM_PLAYERS
        self._num_players = value

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_state_button(self):
        index = self.VALID_NUM_PLAYERS.index(self.num_players) % len(self.VALID_NUM_PLAYERS)
        self.num_players = self.VALID_NUM_PLAYERS[index]
