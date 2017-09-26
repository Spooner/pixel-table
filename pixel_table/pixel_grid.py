import random

from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import numpy as np

from .pixel import Pixel


class PixelGrid(GridLayout):
    WIDTH, HEIGHT = 16, 16

    pixels_rgb = ObjectProperty(np.zeros([WIDTH, HEIGHT, 3]), force_dispatch=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = self.WIDTH

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                pixel = Pixel(grid_pos=(x, y), pixels_rgb=self.pixels_rgb)
                self.add_widget(pixel)

    def clear(self, color=(0, 0, 0)):
        for child in self.children:
            child.color = color

    def pixel(self, x, y):
        return self.children[x + (y * self.WIDTH)]
