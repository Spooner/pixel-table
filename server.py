from __future__ import absolute_import, division, print_function, unicode_literals

import time
from collections import OrderedDict
from traceback import print_exc

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory

from server.messages import PixelTableProtocol
from server.pixel_grid import PixelGrid
from server.modes.matrix_rain import MatrixRain
from server.modes.paint import Paint
from server.modes.pong import Pong


class PixelTableServerFactory(Factory):
    protocol = PixelTableProtocol

    def __init__(self, app):
        self.app = app


class PixelTableServer(object):
    def __init__(self):
        reactor.listenTCP(8000, PixelTableServerFactory(self))

        self._pixel_grid = PixelGrid()

        self._modes = OrderedDict((
            ('paint', Paint(self._pixel_grid)),
            ('matrix_rain', MatrixRain(self._pixel_grid)),
            ('pong', Pong(self._pixel_grid)),
        ))

        self._now = time.time()
        self._mode = None
        self.set_mode("matrix_rain")
        print("\033c")  # Clear terminal

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
            self._pixel_grid.update(dt)

            self._dump(1 / dt)
        except:
            print_exc()
            raise

    def _dump(self, fps):
        print("\033[0;0H", end="")  # Cursor to 0, 0
        self._pixel_grid.dump()
        self._mode.dump()
        print("FPS: %.1f    " % fps)


if __name__ == '__main__':
    PixelTableServer()
