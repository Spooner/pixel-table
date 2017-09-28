#!/usr/bin/env python3

import os

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder

from pixel_table.pixel_table import PixelTable

VERSION = '0.0.1'

if os.environ.get("KIVY_DISABLE_VSYNC") == "1":
    from kivy.config import Config
    print("Running with VSync disabled!")
    Config.set('graphics', 'vsync', '0')
    Config.set('graphics', 'maxfps', '0')
    TICK = 1 / 1000
else:
    TICK = 1 / 60


class PixelTableApp(App):
    def build(self):
        game = PixelTable()
        game.setup()
        Clock.schedule_interval(game.update, TICK)
        return game


if __name__ == '__main__':
    Builder.load_file("pixel_table/pixel_table.kv")
    PixelTableApp().run()
