from .rectangle_sprite import RectangleSprite


class Button(RectangleSprite):
    POSITIONS = {
        "top": {
            "size": (2, 1),
            "positions": ((9, 0), (7, 0), (5, 0)),
            "inputs": (0, 1, 2),
        },
        "left": {
            "size": (1, 2),
            "positions":  ((0, 5), (0, 7), (0, 9)),
            "inputs": (3, 4, 5),
        },
        "bottom": {
            "size": (2, 1),
            "positions": ((5, 15), (7, 15), (9, 15)),
            "inputs": (6, 7, 8),
        },
        "right": {
            "size": (1, 2),
            "positions": ((15, 5), (15, 7), (15, 9)),
            "inputs": (9, 10, 11),
        }
    }
    COLORS = [
        (0.5, 0.25, 0.25),  # Left button (looking in from edge)
        (0.25, 0.25, 0.5),  # Right button (looking in from edge)
        (0.25, 0.5, 0.25),  # Center button (looking in from edge)
    ]

    def __init__(self, side, index):
        config = self.POSITIONS[side]
        x, y = config["positions"][index]
        color = self.COLORS[index]
        width, height = config["size"]
        super(Button, self).__init__(x=x, y=y, width=width, height=height, color=color)
