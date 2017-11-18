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
from server.modes.rain import Rain
from server.modes.pong import Pong
from server.modes.message import Message
from server.modes.game_of_life import GameOfLife
from server.modes.off import Off
from server.modes.tetris import Tetris
from server.modes.title_page import TitlePage
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
        self._modes = [Off, Rain, Pong, Tetris, GameOfLife, Message]
        self._now = time.time()
        self._mode = None
        self._event_queue = []

        self._init_panel_buttons()
        self._init_touch_buttons()

        keyboard = KeyHandler(self)
        stdio.StandardIO(keyboard, sys.stdin.fileno())

        self.set_mode(Rain)

        task.LoopingCall(self.update).start(1 / 25)

        with self.setup_terminal():
            reactor.run()

    def _init_touch_buttons(self):
        pass
    
    @contextmanager
    def setup_terminal(self):
        os.system("clear")  # Clear terminal
        os.system('setterm -cursor off')
        os.system("xset r rate 100 30")
        try:
            term_state = Cbreaktty(sys.stdin.fileno())
        except IOError:
            sys.stderr.write("Error: " + sys.argv[0] + " only for use on interactive ttys\n")
            sys.exit(1)

        try:
            yield
        finally:
            os.system("clear")
            os.system('setterm -cursor on')
            os.system("xset r rate 400 20")
            term_state.return_to_original_state()

    def _init_panel_buttons(self):
        self._mode_button = Button(self.GPIO_MODE)
        self._mode_button.when_pressed = lambda: self.add_to_event_queue("panel_button_press", "mode")
        self._state_button = Button(self.GPIO_STATE)
        self._state_button.when_pressed = lambda: self.add_to_event_queue("panel_button_press", "state")

    def on_mode_button_press(self):
        index = (self._mode.index + 1) % len(self._modes)
        self.set_mode(self._modes[index])

    def on_state_button_press(self):
        self.set_mode(self._mode.mode, self._mode.state_index + 1)

    def set_mode(self, mode, state_index=None, transition=True):
        self._pixel_grid.clear()
        index = self._modes.index(mode)
        smokesignal.clear_all()  # Clear all events in ephemeral objects.

        if transition:
            self._mode = TitlePage(self, mode, index, state_index or mode.DEFAULT_STATE_INDEX)
        else:
            self._mode = mode(index, state_index or mode.DEFAULT_STATE_INDEX)

    def add_to_event_queue(self, event, *args):
        """Store real-time events and pass them out once per frame"""
        self._event_queue.append((event, args))

    def update(self):
        try:
            now = time.time()
            dt = now - self._now
            self._now = now

            for event, args in self._event_queue:
                if event == "panel_button_press":
                    getattr(self, "on_%s_button_press" % args[0])()
                else:
                    smokesignal.emit(event, *args, dt=dt)
            self._event_queue = []

            for index in self._buttons_held:
                self._mode.on_button_held(index, dt)

            self._mode.update(self._pixel_grid, dt)
            self._mode.render(self._pixel_grid)

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
