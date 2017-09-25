import random

from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import numpy as np

from .pixel import Pixel


class PixelGrid(GridLayout):
    WIDTH, HEIGHT = 16, 16

    pixels_rgb = ObjectProperty(np.zeros([WIDTH, HEIGHT, 3]))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = self.WIDTH
        self.pixels_rgb[5][5] = (255, 0, 0)
        self.pixels_rgb[0][0] = (255, 255, 0)

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                pixel = Pixel(grid_pos=(x, y), pixels_rgb=self.pixels_rgb)
                self.add_widget(pixel)
