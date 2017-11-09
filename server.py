#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import time
import os
from traceback import print_exc
import sys
import termios
import tty

from twisted.internet import reactor, task
from twisted.internet.protocol import Factory
from twisted.protocols import basic
from twisted.internet import stdio
from gpiozero import Button

from server.messages import PixelTableProtocol
from server.pixel_grid import PixelGrid
from server.modes.matrix_rain import MatrixRain
from server.modes.pong import Pong


class PixelTableServerFactory(Factory):
    protocol = PixelTableProtocol

    def __init__(self, app):
        self.app = app


# https://stackoverflow.com/questions/23714006/twisted-queue-a-function-interactively
class KeyHandler(basic.LineReceiver):
    class Key(object):
        MODE = '1'
        STATE = '2'

    def __init__(self, app):
        self.setRawMode()  # Switch from line mode to "however much I got" mode
        self._app = app

    def rawDataReceived(self, data):
        key = str(data).lower()[0]
        if key == self.Key.MODE:
            self._app.on_mode_button_press()
        elif key == self.Key.STATE:
            self._app.on_state_button_press()

    def lineReceived(self, line):
        print("LINE:", line)


# # https://stackoverflow.com/questions/23714006/twisted-queue-a-function-interactively
class Cbreaktty(object):
    original_termio = None
    my_termio = None

    def __init__(self, ttyfd):
        if os.isatty(ttyfd):
            self.original_termio = (ttyfd, termios.tcgetattr(ttyfd))
            tty.setcbreak(ttyfd)
            self.my_termio = (ttyfd, termios.tcgetattr(ttyfd))
        else:
            raise IOError

    def return_to_original_state(self):
        tty_, org = self.original_termio
        termios.tcsetattr(tty_, termios.TCSANOW, org)


class PixelTableServer(object):
    GPIO_MODE = 16
    GPIO_STATE = 20

    def __init__(self):
        reactor.listenTCP(8008, PixelTableServerFactory(self))

        self._pixel_grid = PixelGrid()

        self._modes = []
        self._add_mode(MatrixRain)
        self._add_mode(Pong)

        self._now = time.time()
        self._mode = None
        self.set_mode(0)
        print("\033c")  # Clear terminal
        os.system('setterm -cursor off')

        self._init_state_buttons()

        keyboard = KeyHandler(self)
        stdio.StandardIO(keyboard, sys.stdin.fileno())

        task.LoopingCall(self.update).start(1 / 60.0)

        try:
            term_state = Cbreaktty(sys.stdin.fileno())
        except IOError:
            sys.stderr.write("Error: " + sys.argv[0] + " only for use on interactive ttys\n")
            sys.exit(1)

        try:
            reactor.run()
        finally:
            os.system('setterm -cursor on')
            try:
                term_state.return_to_original_state()
            except AttributeError:
                pass

    def _add_mode(self, mode_class):
        self._modes.append(mode_class(pixel_grid=self._pixel_grid, index=len(self._modes)))

    def _init_state_buttons(self):
        self._mode_button = Button(self.GPIO_MODE)
        self._mode_button.when_pressed = self.on_mode_button_press
        self._state_button = Button(self.GPIO_STATE)
        self._state_button.when_pressed = self.on_state_button_press

    def on_mode_button_press(self):
        index = (self._mode.index + 1) % len(self._modes)
        self.set_mode(index)

    def on_state_button_press(self):
        self._mode.on_state_button_press()

    def set_mode(self, index):
        if self._mode is not None:
            self._mode.on_deactivate()

        self._mode = self._modes[index]
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
        lines = ["\033[0;0H"]  # Cursor to 0, 0
        self._pixel_grid.dump(lines)
        self._mode.dump(lines)
        lines.append("%34s" % ("FPS: %2.1f " % fps))
        print("\n".join(lines))


if __name__ == '__main__':
    table = PixelTableServer()
