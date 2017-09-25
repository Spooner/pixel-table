import random

from kivy.uix.gridlayout import GridLayout

from .pixel import Pixel


class PixelGrid(GridLayout):
    WIDTH, HEIGHT = 16, 16

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = self.WIDTH

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                pixel = Pixel(grid_pos=(x, y), color=(random.random(), random.random(), random.random()))
                self.add_widget(pixel)
