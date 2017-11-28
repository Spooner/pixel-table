from __future__ import absolute_import, division, print_function, unicode_literals

import  unicornhathd as unicorn


class Unicorn(object):
    def __init__(self):
        unicorn.rotation(0)
        unicorn.brightness(1.0)
    
    def write_pixels(self, data):
        for y, row in enumerate((data * 255).astype(np.uint8)):
            for x, color in enumerate(row):
                unicorn.set_pixel(x, y, *color)
        unicorn.show()
