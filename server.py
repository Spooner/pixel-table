#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import time
from contextlib import contextmanager
from traceback import print_exc

import smokesignal
from gpiozero import Button as Button
from twisted.internet import reactor, task
from twisted.internet import stdio
from twisted.internet.protocol import Factory

from server.c_break_tty import Cbreaktty
from server.key_handler import KeyHandler
from server.messages import PixelTableProtocol
from server.modes.matrix_rain.matrix_rain import MatrixRain
from server.modes.pong.pong import Pong
from server.pixel_grid import PixelGrid


class PixelTableServerFactory(Factory):
    protocol = PixelTableProtocol

    def __init__(self, app):
        self.app = app


class PixelTableServer(object):
    GPIO_MODE = 16
    GPIO_STATE = 20

    def __init__(self):
        reactor.listenTCP(8008, PixelTableServerFactory(self))

        self._pixel_grid = PixelGrid()

        self._buttons = {}
        self._buttons_held = set()
        self._modes = [MatrixRain, Pong]
        self._now = time.time()
        self._mode = None
        self._event_queue = []

        self._init_panel_buttons()
        self._init_touch_buttons()

        keyboard = KeyHandler(self)
        stdio.StandardIO(keyboard, sys.stdin.fileno())

        self.set_mode(0)

        task.LoopingCall(self.update).start(1 / 30.0)

        with self.setup_terminal():
            reactor.run()

    def _init_touch_buttons(self):
        pass
    
    @contextmanager
    def setup_terminal(self):
        os.system("clear")  # Clear terminal
        os.system('setterm -cursor off')
        try:
            term_state = Cbreaktty(sys.stdin.fileno())
        except IOError:
            sys.stderr.write("Error: " + sys.argv[0] + " only for use on interactive ttys\n")
            sys.exit(1)

        try:
            yield
        finally:
            os.system('setterm -cursor on')
            term_state.return_to_original_state()

    def _init_panel_buttons(self):
        self._mode_button = Button(self.GPIO_MODE)
        self._mode_button.when_pressed = lambda: self.add_to_event_queue("mode_button_press")
        self._state_button = Button(self.GPIO_STATE)
        self._state_button.when_pressed = lambda: self.add_to_event_queue("state_button_press")

    def on_mode_button_press(self):
        index = (self._mode.index + 1) % len(self._modes)
        self.set_mode(index)

    def set_mode(self, index):
        self._pixel_grid.clear()
        smokesignal.clear_all()  # Clear all events in ephemeral objects.
        self._mode = self._modes[index](index=index)

    def add_to_event_queue(self, event, *args):
        """Store real-time events and pass them out once per frame"""
        self._event_queue.append((event, args))

    def update(self):
        try:
            now = time.time()
            dt = now - self._now
            self._now = now

            for event, args in self._event_queue:
                if event == "mode_button_press":
                    self.on_mode_button_press()
                else:
                    smokesignal.emit(event, *args)
            self._event_queue = []

            for index in self._buttons_held:
                self._mode.on_button_held(index, dt)

            smokesignal.emit("update", self._pixel_grid, dt)
            smokesignal.emit("pre_render", self._pixel_grid)  # e.g. clearing or fading previous frame
            smokesignal.emit("render", self._pixel_grid)
            smokesignal.emit("post_render", self._pixel_grid)  # e.g. offsetting current frame

            self._pixel_grid.write()

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
