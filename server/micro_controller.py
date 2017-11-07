from __future__ import absolute_import, division, print_function, unicode_literals

import glob
from time import sleep

import numpy as np
from serial import Serial
from serial.serialutil import SerialException

READY_CHAR = b'R'


class FakeSerial(object):
    def write(self, data):
        sleep(0.001)

    def read(self):
        sleep(0.001)
        return READY_CHAR


class MicroController(object):
    BAUD = 115200

    def __init__(self):
        self._serial = None

    def open(self):
        for device in glob.glob("/dev/ttyUSB*"):
            print("Trying to connect to %s" % device)
            try:
                self._serial = Serial(device, self.BAUD)
                print("Connected to serial port %s" % device)
                self.reset()
                return
            except SerialException:
                pass

        self._serial = FakeSerial()
        print("Failed to connect to a serial port.")

    def reset(self):
        self._serial.setDTR(False)
        sleep(0.022)
        self._serial.setDTR(True)

    def write_pixels(self, data):
        try:
            response = self._serial.read()
            assert response == READY_CHAR
            pixel_bytes = (data * 255).astype(np.uint8).tobytes()
            self._serial.write(pixel_bytes)
        except SerialException:
            pass
