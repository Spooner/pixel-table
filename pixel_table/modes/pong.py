from .mode import Mode


class Sprite:
    def __init__(self, x, y):
        self._x = x
        self._y = y


class RectangleSprite(Sprite):
    WIDTH, HEIGHT = 1, 1
    COLOR = 1, 1, 1

    def render(self, pixels):
        for x in range(self._x, self._x + self.WIDTH):
            for y in range(self._y, self._y + self.HEIGHT):
                pixels.pixel(x, y).color = self.COLOR


class Button(RectangleSprite):
    WIDTH, HEIGHT = 1, 2
    COLOR = (0.5, 0.5, 0.5)


class PongPlayer(RectangleSprite):
    WIDTH, HEIGHT = 1, 4
    COLOR = 1, 1, 1

    def __init__(self, x, up, down):
        super().__init__(x, 6)
        self._up, self._down = up, down

    def update(self, dt):
        pass

    def render(self, pixels):
        super().render(pixels)
        self._up.render(pixels)
        self._down.render(pixels)


class PongBall(RectangleSprite):
    WIDTH, HEIGHT = 1, 1

    def __init__(self):
        super().__init__(7, 7)

    def update(self, dt):
        pass


class Pong(Mode):
    NAME = "Pong"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._players = []
        self._ball = None

    def on_activated(self):
        self._players.append(PongPlayer(1, Button(0, 5), Button(0, 9)))
        self._players.append(PongPlayer(14, Button(15, 5), Button(15, 9)))
        self._ball = PongBall()

    def on_deactivated(self):
        self._players.clear()
        self._ball = None

    def on_button_held(self, button):
        pass

    def update(self, dt):
        self._ball.update(dt)
        for player in self._players:
            player.update(dt)

        self.pixel_grid.clear()
        self._ball.render(self.pixel_grid)
        for player in self._players:
            player.render(self.pixel_grid)
