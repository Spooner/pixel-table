from __future__ import absolute_import, division, print_function, unicode_literals

import time
from collections import OrderedDict
from traceback import print_exc

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory
import numpy as np

from server.messages import PixelTableProtocol
from server.modes.matrix_rain import MatrixRain
from server.modes.paint import Paint


class PixelTableServerFactory(Factory):
    protocol = PixelTableProtocol

    def __init__(self, app):
        self.app = app


class PixelTableServer(object):
    def __init__(self):
        reactor.listenTCP(8000, PixelTableServerFactory(self))

        self._pixel_grid = []

        self._modes = OrderedDict((
            ('paint', Paint(self._pixel_grid)),
            ('matrix_rain', MatrixRain(self._pixel_grid)),
        ))
        self._mode = None
        self._pixel_data = np.zeros((16, 16, 3), np.uint8)

        self._now = time.time()
        self.set_mode("matrix_rain")

        task.LoopingCall(self.update).start(1 / 60.0)

        reactor.run()

    def set_mode(self, name):
        if self._mode is not None:
            self._mode.on_deactivate()

        self._mode = self._modes[name]
        self._mode.on_activate()

    def update(self):
        try:
            now = time.time()
            dt = now - self._now
            self._now = now
            self._mode.on_update(dt)
        except Exception:
            print_exc()
            raise


if __name__ == '__main__':
    PixelTableServer()
