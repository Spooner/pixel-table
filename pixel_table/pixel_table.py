from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from .pixel_grid import PixelGrid


class PixelTable(Widget):
    grid = ObjectProperty(None)
    mode = ObjectProperty(None)
    mode_container = ObjectProperty(None)
    mode_title = ObjectProperty(None)

    def change_mode(self, mode):
        if self.mode is not None:
            self.mode.on_deactivated()

        self.mode = mode
        self.mode_container.clear_widgets()
        self.mode_container.add_widget(mode)
        self.mode.grid = self.grid
        self.mode_title.text = self.mode.NAME
        self.mode.on_activated()

    def update(self, dt):
        self.mode.update(dt)

    def on_pixel_down(self, pixel):
        self.mode.on_pixel_down(pixel)

    def on_pixel_move(self, pixel):
        self.mode.on_pixel_move(pixel)

    def on_pixel_up(self, pixel):
        self.mode.on_pixel_up(pixel)
