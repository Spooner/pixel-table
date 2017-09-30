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
