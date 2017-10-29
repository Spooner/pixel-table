from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView

from .mode import Mode


class Tool(ToggleButton):
    def __init__(self, **kwargs):
        super(Tool, self).__init__(**kwargs)
        self.group = "paint_tools"
        self.text = type(self).__name__
        self.allow_no_selection = False

    def on_touch_up(self, touch):
        self.root.tool = self


class Paint(Mode):
    NAME = "Paint"

    color = ObjectProperty(None)
    tool = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Paint, self).__init__(**kwargs)

        self._data = None

    def open_color_dialog(self, *args):
        PaintColorPicker(self).open()

    def on_activated(self):
        if self._data is not None:
            self._pixel_grid.import_data(self._data)

    def on_deactivated(self):
        self._data = self._pixel_grid.export_data()


class PaintColorPicker(ModalView):
    color_picker = ObjectProperty(None)

    def __init__(self, paint, **kwargs):
        super(PaintColorPicker, self).__init__(**kwargs)
        self._paint = paint

    def pick(self):
        self._paint.color.color = self.color_picker.color[:3]
        self.dismiss()
