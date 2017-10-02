class Sprite:
    def __init__(self, x, y, width=1, height=1, color=(1, 1, 1)):
        self._x, self._y = x, y
        self._width, self._height = width, height
        self._color = color

    @property
    def int_position(self):
        return int(round(self._x)), int(round(self._y))

    def collide_point(self, x, y):
        return (self._x <= x < self._x + self._width) and (self._y <= y < self._y + self._height)
