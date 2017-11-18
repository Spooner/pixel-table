from __future__ import absolute_import, division, print_function, unicode_literals

import os

from PIL import Image

from .sprite import Sprite


class SpriteSheet(Sprite):
    _all_images = {}

    def __init__(self, x, y, name, num_frames=1, frame=0):
        super(SpriteSheet, self).__init__(x=x, y=y)

        self._name = name
        self._num_frames = num_frames
        self._points = None
        self._frame = None

        if name not in self._all_images:
            self._all_images[name] = self._load_data_from_image()

        self.frame = frame

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value % self._num_frames
        frames, self._width, self._height = self._all_images[self._name]
        self._points = frames[self._frame]

    def _load_data_from_image(self):
        image = Image.open(os.path.join(os.path.dirname(__file__), "images", "%s.png" % self._name))

        width, height = image.size[0] // self._num_frames, image.size[1]

        frames = [{} for _ in range(self._num_frames)]
        for frame in range(self._num_frames):
            for x in range(frame * width, (frame + 1) * width):
                for y in range(0, image.size[1]):
                    r, g, b, a = image.getpixel((x, y))
                    if a >= 128:
                        frames[frame][x, y] = (r / 255, g / 255, b / 255)

        return [frames, width, height]

    def render(self, pixel_grid):
        base_x, base_y = self.int_position
        for (offset_x, offset_y), color in self._points.items():
            screen_x, screen_y = base_x + offset_x, base_y + offset_y
            if 0 <= screen_x < 16 and 0 <= screen_y < 16:
                pixel_grid.pixel(screen_x, screen_y).color = color
