from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ColorProperty
from kivy.app import App


class Pixel(Widget):
    grid_x = NumericProperty(0)
    grid_y = NumericProperty(0)
    grid_pos = ReferenceListProperty(grid_x, grid_y)

    color = ColorProperty((0, 0, 0))
    pixels_rgb = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Pixel, self).__init__(**kwargs)
        self.bind(color=self.update_color)
        self.color = tuple(self.pixels_rgb[self.grid_x][self.grid_y])

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().root.on_pixel_move(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().root.on_pixel_down(self)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            App.get_running_app().root.on_pixel_up(self)

    def update_color(self, obj, color):
        """Update raw color bytes (255, 255, 255) from local color (1.0, 1.0, 1.0)"""
        color_bytes = tuple(c * 255 for c in color[:3])
        self.pixels_rgb[self.grid_x][self.grid_y] = color_bytes
