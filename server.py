from __future__ import absolute_import, division, print_function, unicode_literals

import time

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory
import numpy as np

from server.messages import PixelTableProtocol
from server.modes.matrix_rain import MatrixRain
from server.modes.paint import Paint

import math
from collections import OrderedDict

import numpy as np
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from server.pixel_controller import PixelController
from .pixel import Pixel




class PixelTableServerFactory(Factory):
    protocol = PixelTableProtocol

    def __init__(self, app):
        self.app = app


class PixelTableServer(object):
    def __init__(self):
        reactor.listenTCP(8000, PixelTableServerFactory(self))

        self._pixel_grid = []

        self._modes = {
            'paint': Paint(self._pixel_grid),
            'matrix_rain': MatrixRain(self._pixel_grid),
        }
        self._mode = None
        self._pixel_data = np.zeros((16, 16, 3), np.uint8)

        self._now = time.time()
        self.set_mode("paint")

        task.LoopingCall(self.update).start(1 / 60.0)

        reactor.run()

    def set_mode(self, name):
        if self._mode is not None:
            self._mode.on_deactivate()

        self._mode = self._modes[name]
        self._mode.on_activate()

    def update(self):
        now = time.time()
        dt = now - self._now
        self._now = now
        self._mode.on_update(dt)


if __name__ == '__main__':
    PixelTableServer()
