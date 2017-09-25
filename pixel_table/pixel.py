from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ColorProperty
from kivy.app import App


class Pixel(Widget):
    grid_x = NumericProperty(0)
    grid_y = NumericProperty(0)
    grid_pos = ReferenceListProperty(grid_x, grid_y)

    color = ColorProperty()

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().root.on_pixel(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().root.on_pixel(self)
