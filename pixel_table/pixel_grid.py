
from collections import OrderedDict
import math

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
import numpy as np
from serial import Serial
from serial.serialutil import SerialException


class Pixel:
    def __init__(self, x, y, pixel_grid):
        self._x, self._y = x, y
        self._pixel_grid = pixel_grid
        self.color_on_canvas = None

    @property
    def color(self):
        return self._pixel_grid.get_color(self._x, self._y)

    @color.setter
    def color(self, color):
        self._pixel_grid.set_color(self._x, self._y, color)
        self.color_on_canvas.rgb = color

    def __str__(self):
        return "<Pixel ({}, {}) {}>".format(self._x, self._y, self.color)


class PixelGrid(Widget):
    WIDTH, HEIGHT = 16, 16

    data = ObjectProperty(np.zeros([WIDTH, HEIGHT, 3]), force_dispatch=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._cell_width = self.width / self.WIDTH

        self._pixels = OrderedDict()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self._pixels[x, y] = Pixel(x, y, pixel_grid=self)

        self.update_canvas()

        self.bind(size=self.update_canvas)
        self.bind(pos=self.update_canvas)

        self.register_event_type("on_pixel_down")
        self.register_event_type("on_pixel_move")
        self.register_event_type("on_pixel_up")

    @property
    def pixels(self):
        return self._pixels.values()

    def clear(self, color=(0, 0, 0)):
        for pixel in self.pixels:
            pixel.color = color

    def pixel(self, x, y):
        return self._pixels[x, y]

    def export_data(self):
        return self.data.copy()

    def import_data(self, data):
        self.data = data
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        self._cell_width = self.width / self.WIDTH
        draw_size = (self._cell_width - 1, self._cell_width - 1)

        with self.canvas:
            for (x, y), pixel in self._pixels.items():
                pixel.color_on_canvas = Color(*pixel.color)
                Rectangle(pos=(self.x + x * self._cell_width, self.y + y * self._cell_width), size=draw_size)

    def pixel_at(self, position):
        x = min(max(math.floor(position[0] / self._cell_width), 0), self.WIDTH - 1)
        y = min(max(math.floor(position[1] / self._cell_width), 0), self.HEIGHT - 1)
        return self._pixels[x, y]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_pixel_down", self.pixel_at(touch.pos))

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_pixel_move", self.pixel_at(touch.pos))

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_pixel_up", self.pixel_at(touch.pos))

    def on_pixel_down(self, pixel):
        pass

    def on_pixel_move(self, pixel):
        pass

    def on_pixel_up(self, pixel):
        pass

    def get_color(self, x, y):
        return self.data[x][y]

    def set_color(self, x, y, color):
        self.data[x][y] = color

    def fade(self, amount):
        for pixel in self.pixels:
            r, g, b = pixel.color
            pixel.color = max(r - amount, 0), max(g - amount, 0), max(b - amount, 0)

    def write_pixels_to_serial(self):
        try:
            serial = Serial("/dev/ttyUSB0", 115200)
            serial.write(self.data.astype(np.uint8).tobytes())
        except SerialException:
            print("Failed to send serial data.")
