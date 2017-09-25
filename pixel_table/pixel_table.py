from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from .pixel_grid import PixelGrid
from .modes.paint  import Paint


class PixelTable(Widget):
    grid = ObjectProperty(None)
    mode = ObjectProperty(None)

    def update(self, dt):
        self.mode.update(dt)

    def on_pixel_down(self, pixel):
        self.mode.on_pixel_down(pixel)

    def on_pixel_move(self, pixel):
        self.mode.on_pixel_move(pixel)

    def on_pixel_up(self, pixel):
        self.mode.on_pixel_up(pixel)
