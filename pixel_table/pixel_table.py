from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from .pixel_grid import PixelGrid
from .modes.paint import Paint
from .modes.matrix_rain import MatrixRain


class PixelTable(Widget):
    pixel_grid = ObjectProperty(None)
    mode = ObjectProperty(None)
    mode_container = ObjectProperty(None)
    mode_dropdown = ObjectProperty(None)
    mode_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pixel_grid.bind(on_pixel_down=self.on_pixel_down)
        self.pixel_grid.bind(on_pixel_move=self.on_pixel_move)
        self.pixel_grid.bind(on_pixel_up=self.on_pixel_up)

    def setup(self):
        modes = [m() for m in [Paint, MatrixRain]]

        for mode in modes:
            self._add_mode(mode)

        self.change_mode(modes[0])

    def _add_mode(self, mode):
        button = Button(text=mode.NAME, size_hint_y=None, height=40)
        button.bind(on_release=lambda btn: self.change_mode(mode))
        self.mode_dropdown.add_widget(button)

    def change_mode(self, mode):
        if self.mode is not None:
            self.mode.on_deactivated()

        self.mode = mode
        self.mode_button.text = self.mode.NAME
        self.mode_dropdown.dismiss()
        self.mode_container.clear_widgets()
        self.mode_container.add_widget(self.mode)
        self.mode.pixel_grid = self.pixel_grid
        self.mode.on_activated()

    def update(self, dt):
        self.mode.update(dt)
        self.pixel_grid.update()

    def on_pixel_down(self, sender, pixel):
        self.mode.on_pixel_down(pixel)

    def on_pixel_move(self, sender, pixel):
        self.mode.on_pixel_move(pixel)

    def on_pixel_up(self, sender, pixel):
        self.mode.on_pixel_up(pixel)
