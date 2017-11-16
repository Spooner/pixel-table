from __future__ import absolute_import, division, print_function, unicode_literals

from server.modes.mode import Mode
from .player import Player
from .ball import Ball


class Pong(Mode):
    VALUE_NAMES = ["num_players"]
    VALID_NUM_PLAYERS = [2, 4]
    DEFAULT_NUM_PLAYERS = 2

    def __init__(self, index):
        super(Pong, self).__init__(index)
        self._num_players = self.DEFAULT_NUM_PLAYERS
        self._players = []
        self._ball = None
        self._start_game()

    @property
    def num_players(self):
        return self._num_players

    @num_players.setter
    def num_players(self, value):
        assert value in self.VALID_NUM_PLAYERS
        self._num_players = value

    def _start_game(self):
        self._players = []
        for i in range(self._num_players):
            self._players.append(Player(i))

        self._ball = Ball(list(p.paddle for p in self._players))

    def on_state_button_press(self):
        index = (self.VALID_NUM_PLAYERS.index(self.num_players) + 1) % len(self.VALID_NUM_PLAYERS)
        self.num_players = self.VALID_NUM_PLAYERS[index]
        self._start_game()

    def on_touch_button_held(self, player_index, button_index, dt):
        self._players[player_index].on_touch_button_held(button_index, dt)

    def on_pre_render(self, pixel_grid):
        pixel_grid.clear()
