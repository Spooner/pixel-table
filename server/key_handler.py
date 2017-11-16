from __future__ import absolute_import, division, print_function, unicode_literals

from twisted.protocols import basic
import smokesignal

from server.sprites.touch_button import TouchButton


# https://stackoverflow.com/questions/23714006/twisted-queue-a-function-interactively
class KeyHandler(basic.LineReceiver):
    MODE_BUTTON = b'1'
    STATE_BUTTON = b'2'

    TOUCH_BUTTONS = {
        # Bottom side, player 0
        b'X': (0, TouchButton.LEFT),
        b'C': (0, TouchButton.CENTER),
        b'V': (0, TouchButton.RIGHT),

        # Top side, player 1
        b'R': (1, TouchButton.LEFT),
        b'E': (1, TouchButton.CENTER),
        b'W': (1, TouchButton.RIGHT),

        # Left side, player 2
        b'Q': (2, TouchButton.LEFT),
        b'A': (2, TouchButton.CENTER),
        b'Z': (2, TouchButton.RIGHT),

        # Right side, player 3
        b'B': (3, TouchButton.LEFT),
        b'G': (3, TouchButton.CENTER),
        b'T': (3, TouchButton.RIGHT),
    }

    def __init__(self, app):
        self.setRawMode()  # Switch from line mode to "however much I got" mode
        self._app = app

    def rawDataReceived(self, data):
        key = str(data).upper()[0]
        if key == self.MODE_BUTTON:
            self._app.add_to_event_queue("panel_button_press", "mode")
        elif key == self.STATE_BUTTON:
            self._app.add_to_event_queue("panel_button_press", "state")
        elif key in self.TOUCH_BUTTONS:
            self._app.add_to_event_queue("touch_button_held", *self.TOUCH_BUTTONS[key])

    def lineReceived(self, line):
        pass
