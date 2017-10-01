import glob
from time import sleep

import numpy as np
from serial import Serial
from serial.serialutil import SerialException


class DummySerial:
    def write(self, data):
        sleep(0.02)

    def read(self):
        sleep(0.02)
        return b'R'


class PixelController:
    BAUD = 115200
    READY_CHAR = b'R'

    def __init__(self):
        self._serial = None

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
        assert self._serial.read() == self.READY_CHAR
        pixel_bytes = (data * 255).astype(np.uint8).tobytes()
        self._serial.write(pixel_bytes)
