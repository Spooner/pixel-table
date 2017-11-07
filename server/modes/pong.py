from __future__ import absolute_import, division, print_function, unicode_literals

from .mode import Mode


class Pong(Mode):
    VALUE_NAMES = ["num_players"]
    VALID_NUM_PLAYERS = [2, 4]
    DEFAULT_NUM_PLAYERS = 2

    def __init__(self, pixel_grid, index):
        super(Pong, self).__init__(pixel_grid, index)

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

    def on_state_button_press(self):
        index = (self.VALID_NUM_PLAYERS.index(self.num_players) + 1) % len(self.VALID_NUM_PLAYERS)
        self.num_players = self.VALID_NUM_PLAYERS[index]
