from __future__ import absolute_import, division, print_function, unicode_literals

import os


def root(*path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *path))
