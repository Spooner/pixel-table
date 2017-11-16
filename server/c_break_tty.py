from __future__ import absolute_import, division, print_function, unicode_literals

import os
import termios
import tty


# https://stackoverflow.com/questions/23714006/twisted-queue-a-function-interactively
class Cbreaktty(object):
    original_termio = None
    my_termio = None

    def __init__(self, ttyfd):
        if os.isatty(ttyfd):
            self.original_termio = (ttyfd, termios.tcgetattr(ttyfd))
            tty.setcbreak(ttyfd)
            self.my_termio = (ttyfd, termios.tcgetattr(ttyfd))
        else:
            raise IOError

    def return_to_original_state(self):
        tty_, org = self.original_termio
        termios.tcsetattr(tty_, termios.TCSANOW, org)
