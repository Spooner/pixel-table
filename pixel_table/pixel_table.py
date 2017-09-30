from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from .pixel_grid import PixelGrid
from .modes.paint import Paint
from .modes.matrix_rain import MatrixRain


class PixelTable(Widget):
    pixel_grid = ObjectProperty(None)
    mode = ObjectProperty(None)
    mode_container = ObjectProperty(None)
    mode_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._modes = self._mode_dropdown = None

        self.pixel_grid.bind(on_pixel_down=self.on_pixel_down)
        self.pixel_grid.bind(on_pixel_move=self.on_pixel_move)
        self.pixel_grid.bind(on_pixel_up=self.on_pixel_up)

    def setup(self):
        self._modes = [
            Paint(),
            MatrixRain(),
        ]
        self._mode_dropdown = ModeDropDown(self._modes, self.change_mode)

        self.change_mode(self._modes[0])

    def change_mode(self, mode):
        if self.mode is not None:
            self.mode.on_deactivated()

        self.mode = mode
        self.mode_button.text = self.mode.NAME
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

    def open_dropdown(self):
        self._mode_dropdown.open(self.mode_button)


class ModeDropDown(DropDown):
    def __init__(self, modes, change_mode, **kwargs):
        super().__init__(**kwargs)

        self._change_mode = change_mode
        for mode in modes:
            self._add_mode(mode)

    def _add_mode(self, mode):
        button = Button(text=mode.NAME, size_hint_y=None, height=40)
        button.bind(on_release=lambda sender: self.mode_picked(mode))
        self.add_widget(button)

    def mode_picked(self, mode):
        self._change_mode(mode)
        self.dismiss()
