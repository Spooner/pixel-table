from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from .pixel_grid import PixelGrid
from .tools import Tools
from .current_color  import CurrentColor


class PixelTable(Widget):
    grid = ObjectProperty(None)
    current_color = ObjectProperty(None)

    def update(self, dt):
        pass
        #self.grid.update(dt)
