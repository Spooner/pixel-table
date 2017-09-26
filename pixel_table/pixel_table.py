from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from .pixel_grid import PixelGrid


class PixelTable(Widget):
    grid = ObjectProperty(None)
    mode = ObjectProperty(None)
    mode_container = ObjectProperty(None)
    mode_dropdown = ObjectProperty(None)
    mode_button = ObjectProperty(None)

    def init_modes(self, mode_classes, initial_mode_class):
        for mode_class in mode_classes:
            self._add_mode(mode_class)

        self.change_mode(initial_mode_class)

    def _add_mode(self, mode):
        button = Button(text=mode.NAME, size_hint_y=None, height=40)
        button.bind(on_release=lambda btn: self.change_mode(mode))
        self.mode_dropdown.add_widget(button)

    def change_mode(self, mode_class):
        if self.mode is not None:
            self.mode.on_deactivated()

        self.mode = mode_class()
        self.mode_button.text = self.mode.NAME
        self.mode_dropdown.dismiss()
        self.mode_container.clear_widgets()
        self.mode_container.add_widget(self.mode)
        self.mode.grid = self.grid
        self.mode.on_activated()

    def update(self, dt):
        self.mode.update(dt)

    def on_pixel_down(self, pixel):
        self.mode.on_pixel_down(pixel)

    def on_pixel_move(self, pixel):
        self.mode.on_pixel_move(pixel)

    def on_pixel_up(self, pixel):
        self.mode.on_pixel_up(pixel)
