from kivy.uix.boxlayout import BoxLayout


class Mode(BoxLayout):
    """Abstract base for Mode widgets"""

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_pixel_down(self, pixel):
        pass

    def on_pixel_move(self, pixel):
        pass

    def on_pixel_up(self, pixel):
        pass

    def update(self, dt):
        pass
