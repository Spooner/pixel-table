#! /usr/bin/env python
# https://gist.github.com/MicahElliott/719710
# Comment by TerrorBite gave cleaner code.

#---------------------------------------------------------------------

# Default color levels for the color cube
CUBE_LEVELS = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]

# Generate a list of midpoints of the above list
SNAPS = [(x + y) / 2 for x, y in zip(CUBE_LEVELS, [0] + CUBE_LEVELS)[1:]]


def rgb2short(rgb):
    """ Converts RGB values to the nearest equivalent xterm-256 color.
    """
    # Using list of snap points, convert RGB value to cube indexes
    r, g, b = (sum(1 for s in SNAPS if s < c) for c in rgb)

    # Simple color-cube transform
    return (r * 36) + (g * 6) + b + 16
