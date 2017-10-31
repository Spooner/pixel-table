from __future__ import absolute_import, division, print_function, unicode_literals

import glob
from time import sleep

import numpy as np
from serial import Serial
from serial.serialutil import SerialException

READY_CHAR = b'R'


class FakeSerial(object):
    def write(self, data):
        sleep(0.01)

    def read(self):
        sleep(0.01)
        return READY_CHAR


class PixelController(object):
    BAUD = 460800

    def __init__(self):
        self._serial = None

    def open(self):
        for device in glob.glob("/dev/ttyUSB*"):
            print("Trying to connect to %s" % device)
            try:
                self._serial = Serial(device, self.BAUD)
                print("Connected to serial port %s" % device)
                return
            except SerialException:
                pass

        self._serial = FakeSerial()
        print("Failed to connect to a serial port.")

    def write_pixels(self, data):
        assert self._serial.read() == READY_CHAR
        pixel_bytes = (data * 255).astype(np.uint8).tobytes()
        self._serial.write(pixel_bytes)
