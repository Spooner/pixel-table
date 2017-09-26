from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, ColorProperty, StringProperty

from .mode import Mode


class Paint(Mode):
    class Tools:
        PENCIL = "pencil"
        ERASER = "eraser"
        DROPPER = "dropper"

    NAME = "Paint"

    current_color = ObjectProperty(None)
    current_tool = StringProperty(Tools.PENCIL)
    grid = ObjectProperty(None)

    def on_activated(self):
        self.grid.clear()
        self.grid.children[0].color = (255, 255, 0)
        self.grid.children[12].color = (0, 255, 0)
        self.grid.children[39].color = (255, 0, 0)

    def on_deactivated(self):
        pass

    def on_pixel_down(self, pixel):
        self._on_pixel(pixel)

    def on_pixel_move(self, pixel):
        self._on_pixel(pixel)

    def _on_pixel(self, pixel):
        if self.current_tool == self.Tools.PENCIL:
            pixel.color = self.current_color.color
        elif self.current_tool == self.Tools.DROPPER:
            self.current_color.color = pixel.color
        elif self.current_tool == self.Tools.ERASER:
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
