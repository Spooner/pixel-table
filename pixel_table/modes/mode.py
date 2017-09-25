from kivy.uix.widget import Widget


class Mode(Widget):
    """Abstract base for Mode widgets"""

    def on_pixel(self, pixel):
        pass

    def update(self, dt):
        pass
