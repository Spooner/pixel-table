from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from Adafruit_MPR121.MPR121 import MPR121
from bitarray import bitarray
import smokesignal

_logger = logging.getLogger(__name__)


class MockCapTouch(object):
    def __init__(self):
        pass

    def begin(self):
        pass

    def touched(self):
        return 0b000000000000


class TouchButtons(object):
    NUM_TOUCHES = 12
    PLAYER_AND_BUTTON_FOR_TOUCH = {
        0: (0, 0),
        1: (0, 1),
        2: (0, 2),
        3: (1, 0),
        4: (1, 1),
        5: (1, 2),
        6: (2, 0),
        7: (2, 1),
        8: (2, 2),
        9: (3, 0),
        10: (3, 1),
        11: (3, 2),
    }

    def __init__(self):
        self._touches = bitarray(self.NUM_TOUCHES)
        self._cap_touch = MPR121()
        try:
            if self._cap_touch.begin():
                self._cap_touch.touched()  # Just clear out any current changes.
                _logger.info("Capacitive touch system engaged")
            else:
                raise RuntimeError
        except (RuntimeError, IOError):
            _logger.warning("Capacitive touch system failed; using mock")
            self._cap_touch = MockCapTouch()

    def emit_events(self, dt):
        touches = bitarray(self.NUM_TOUCHES)
        cap_touches = self._cap_touch.touched()
        for i in range(self.NUM_TOUCHES):
            touched = cap_touches & (1 << i)
            touches[i] = touched

            player, button = self.PLAYER_AND_BUTTON_FOR_TOUCH[i]
            if touched and not self._touches[i]:
                smokesignal.emit("touch_button_press", player, button)

            if touched:
                smokesignal.emit("touch_button_held", player, button, dt)

            if not touched and self._touches[i]:
                smokesignal.emit("touch_button_release", player, button)

        self._touches = touches
