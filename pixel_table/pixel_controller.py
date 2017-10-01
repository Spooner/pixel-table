import glob
from time import sleep

import numpy as np
from serial import Serial
from serial.serialutil import SerialException


class DummySerial:
    def write(self, data):
        sleep(0.01)

    def read(self):
        sleep(0.01)
        return b'X'


class PixelController:
    BAUD = 230400

    def __init__(self):
        self._serial = None
        self._brightness = 0.25

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = min(1, max(value, 0))

    def open(self):
        for device in glob.glob("/dev/ttyUSB*"):
            print("Trying to connect to %s" % device)
            try:
                self._serial = Serial(device, self.BAUD)
                print("Connected to serial port %s" % device)
                return
            except SerialException:
                pass

        self._serial = DummySerial()
        print("Failed to connect to a serial port.")

    def write_pixels(self, data):
        assert self._serial.read() == b'X'
        pixel_bytes = (data * int(255 * self._brightness)).astype(np.uint8).tobytes()
        self._serial.write(pixel_bytes)
