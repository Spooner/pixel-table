import random
import math

from kivy.properties import ObjectProperty

from .mode import Mode


class MatrixRain(Mode):
    NAME = "Matrix Rain"

    num_drops = ObjectProperty(None)
