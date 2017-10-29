from .sprite import Sprite


class RectangleSprite(Sprite):
    def render(self, pixels):
        x, y = self.int_position
        for xx in range(x, x + self._width):
            for yy in range(y, y + self._height):
                pixels.pixel(xx, yy).color = self._color
