from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView

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

    def on_pixel_held(self, pixel, dt):
        pass

    def on_touch_up(self, touch):
        self.root.tool = self
    
    
class Pencil(Tool):
    def on_pixel_held(self, pixel, dt):
        pixel.color = self.root.color.color

        
class Eraser(Tool):
    def on_pixel_held(self, pixel, dt):
        pixel.color = 0, 0, 0
    
    
class Dropper(Tool):
    def on_pixel_held(self, pixel, dt):
        self.root.color.color = pixel.color
    

class Paint(Mode):
    NAME = "Paint"

    color = ObjectProperty(None)
    tool = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = None

    def open_color_dialog(self, *args):
        PaintColorPicker(self).open()

    def on_activated(self):
        if self._data is not None:
            self._pixel_grid.import_data(self._data)

    def on_deactivated(self):
        self._data = self._pixel_grid.export_data()

    def on_pixel_down(self, pixel):
        self.tool.on_pixel_down(pixel)

    def on_pixel_move(self, pixel):
        self.tool.on_pixel_move(pixel)

    def on_pixel_up(self, pixel):
        self.tool.on_pixel_up(pixel)

    def on_pixel_held(self, pixel, dt):
        self.tool.on_pixel_held(pixel, dt)


class PaintColorPicker(ModalView):
    color_picker = ObjectProperty(None)

    def __init__(self, paint, **kwargs):
        super().__init__(**kwargs)
        self._paint = paint

    def pick(self):
        self._paint.color.color = self.color_picker.color[:3]
        self.dismiss()
