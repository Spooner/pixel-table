#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

# https://gist.github.com/MicahElliott/719710

# Unhandled colours.
CLUT = [
    ('01',  '800000'),
    ('02',  '008000'),
    ('03',  '808000'),
    ('04',  '000080'),
    ('05',  '800080'),
    ('06',  '008080'),
    ('07',  'c0c0c0'),
]


def rgb2short(r, g, b):
    """ Find the closest xterm-256 approximation to the given RGB value.
    @param r: red 0-1
    @poram g: green 0-1
    @param b: green 0-1
    @returns: String between 0 and 255, compatible with xterm.
    """
    assert 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1, (r, g, b)

    if r == g == b:
        # greyscale 0 and 232-255 ("black" is actually at 16, not 231)
        value = int(round((r * 24) + 231))
        if value == 231:
            value = 16
    else:
        # color 16-231
        value = int(round(36 * (r * 5) + 6 * (g * 5) + (b * 5) + 16))

    return value
