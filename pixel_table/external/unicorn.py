from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np


class Unicorn(object):
    def __init__(self):
        import unicornhathd as unicorn

        unicorn.rotation(0)
        unicorn.brightness(1.0)
    
    def write_pixels(self, data):
        import unicornhathd as unicorn

        for y, row in enumerate((data * 255).astype(np.uint8)):
            for x, color in enumerate(row):
                unicorn.set_pixel(x, y, *color)
        unicorn.show()
