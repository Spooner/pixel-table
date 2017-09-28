#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder

from pixel_table.pixel_table import PixelTable

VERSION = '0.0.1'


class PixelTableApp(App):
    def build(self):
        game = PixelTable()
        game.setup()
        Clock.schedule_interval(game.update, 1 / 60)
        return game


if __name__ == '__main__':
    Builder.load_file("pixel_table/pixel_table.kv")
    PixelTableApp().run()
