from __future__ import absolute_import, division, print_function, unicode_literals

from .rectangle_sprite import RectangleSprite


class TouchButton(RectangleSprite):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    POSITIONS = {
        1: {  # TOP
            "size": (2, 1),
            "positions": ((9, 0), (7, 0), (5, 0)),
            "inputs": (0, 1, 2),
        },
        2: {  # LEFT
            "size": (1, 2),
            "positions":  ((0, 5), (0, 7), (0, 9)),
            "inputs": (3, 4, 5),
        },
        0: {  # BOTTOM
            "size": (2, 1),
            "positions": ((5, 15), (7, 15), (9, 15)),
            "inputs": (6, 7, 8),
        },
        3: {  # RIGHT
            "size": (1, 2),
            "positions": ((15, 9), (15, 7), (15, 5)),
            "inputs": (9, 10, 11),
        }
    }
    COLORS = [
        (0.5, 0.25, 0.25),  # Left button - RED (looking in from edge)
        (0.25, 0.5, 0.25),  # Right button - GREEN (looking in from edge)
        (0.25, 0.25, 0.5),  # Center button - BLUE (looking in from edge)
    ]

    def __init__(self, player_index, button_index):
        self._player_index, self._button_index = player_index, button_index
        config = self.POSITIONS[player_index]
        x, y = config["positions"][button_index]
        self._default_color = self.COLORS[button_index]
        self._pressed_color = list(c + 0.25 for c in self._default_color)
        self._is_pressed = False
        width, height = config["size"]
        super(TouchButton, self).__init__(x=x, y=y, width=width, height=height, color=self._default_color)

    def on_touch_button_held(self, player_index, button_index, dt):
        if player_index != self._player_index or button_index != self._button_index:
            return

        self._is_pressed = True

    @property
    def color(self):
        if self._is_pressed:
            return self._pressed_color
        else:
            return self._default_color

    def on_post_render(self, pixel_grid):
        self._is_pressed = False
