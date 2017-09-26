#!/usr/bin/env python3

import os

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder

from pixel_table.pixel_table import PixelTable
from pixel_table.modes.paint import Paint
from pixel_table.modes.matrix_rain import MatrixRain

VERSION = '0.0.1'

if os.environ.get("PIXEL_TABLE_DEBUG"):
    from kivy.config import Config
    Config.set('modules', 'monitor', '')


class PixelTableApp(App):
    def build(self):
        game = PixelTable()
        game.init_modes([Paint(), MatrixRain()])

        Clock.schedule_interval(game.update, 1 / 60)
        return game


if __name__ == '__main__':
    Builder.load_file("pixel_table/pixel_table.kv")
    PixelTableApp().run()
