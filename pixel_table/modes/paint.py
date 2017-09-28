from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
import numpy as np

from .mode import Mode


class Tool(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = "paint_tools"
        self.text = type(self).__name__
        self.allow_no_selection = False

    def on_pixel_down(self, pixel):
        pass
        
    def on_pixel_move(self, pixel):
        pass
        
    def on_pixel_up(self, pixel):
        pass
    
    def on_pixel_held(self, pixel):
        pass

    def on_touch_up(self, touch):
        self.root.tool = self
    
    
class Pencil(Tool):
    def on_pixel_held(self, pixel):
        pixel.set_color_with_update(self.root.color.color)

        
class Eraser(Tool):
    def on_pixel_held(self, pixel):
        pixel.set_color_with_update((0, 0, 0))
    
    
class Dropper(Tool):
    def on_pixel_held(self, pixel):
        self.root.color.color = pixel.color
    

class Paint(Mode):
    NAME = "Paint"

    color = ObjectProperty(None)
    tool = ObjectProperty(None)
    pixel_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = None

    def on_activated(self):
        if self._data is not None:
            self.pixel_grid.import_data(self._data)

    def on_deactivated(self):
        self._data = self.pixel_grid.export_data()

    def on_pixel_down(self, pixel):
        self.tool.on_pixel_down(pixel)
        self.tool.on_pixel_held(pixel)

    def on_pixel_move(self, pixel):
        self.tool.on_pixel_move(pixel)
        self.tool.on_pixel_held(pixel)
        
    def on_pixel_up(self, pixel):
        self.tool.on_pixel_up(pixel)
