#!/usr/bin/env python2

from __future__ import absolute_import, division, print_function, unicode_literals

# install_twisted_rector() must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from twisted.internet import reactor

from .pixel_table import PixelTable
from .client_factory import PixelTableClientFactory

VERSION = '0.0.1'


class PixelTableClient(App):
    def build(self):
        game = PixelTable()
        game.setup()
        Clock.schedule_interval(game.update, 1 / 60)

        return game

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, PixelTableClientFactory(self))

    def handle_response(self, response):
        pass


if __name__ == '__main__':
    Builder.load_file("pixel_table/pixel_table.kv")
    PixelTableClient().run()
