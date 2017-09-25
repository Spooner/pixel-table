from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, ColorProperty, StringProperty

from .mode import Mode


class Paint(Mode):
    PENCIL = "pencil"
    ERASER = "eraser"
    DROPPER = "dropper"

    current_color = ObjectProperty(None)
    current_tool = StringProperty(PENCIL)

    def on_activated(self):
        self.pixels_rgb[5][5] = (255, 0, 0)
        self.pixels_rgb[0][0] = (255, 255, 0)
        self.pixels_rgb[15][15] = (0, 255, 0)

    def on_deactivated(self):
        pass

    def on_pixel_down(self, pixel):
        self._on_pixel(pixel)

    def on_pixel_move(self, pixel):
        self._on_pixel(pixel)

    def _on_pixel(self, pixel):
        if self.current_tool == self.PENCIL:
            pixel.color = self.current_color.color
        elif self.current_tool == self.DROPPER:
            self.current_color.color = pixel.color
        elif self.current_tool == self.ERASER:
            pixel.color = (0, 0, 0)
        else:
            raise ValueError(self.current_tool)

    def update(self, dt):
        pass


class PaintTools(GridLayout):
    def pick_tool(self, touch, name):
        if self.collide_point(*touch.pos):
            self.parent.parent.current_tool = name


class PaintColor(Widget):
    color = ColorProperty(None)
