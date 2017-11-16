from __future__ import absolute_import, division, print_function, unicode_literals

import os
import termios
import tty


# https://stackoverflow.com/questions/23714006/twisted-queue-a-function-interactively
class Cbreaktty(object):
    original_termio = None
    my_termio = None

    def __init__(self, tty_fd):
        if os.isatty(tty_fd):
            self.original_termio = (tty_fd, termios.tcgetattr(tty_fd))
            tty.setcbreak(tty_fd)
            self.my_termio = (tty_fd, termios.tcgetattr(tty_fd))
        else:
            raise IOError

    def return_to_original_state(self):
        tty_, org = self.original_termio
        termios.tcsetattr(tty_, termios.TCSANOW, org)
