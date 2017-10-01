import glob
import sys
from time import sleep

import numpy as np
from serial import Serial
from serial.serialutil import SerialException


class DummySerial:
    def write(self, data):
        sleep(0.01)

    def reset_input_buffer(self):
        pass

    def reset_output_buffer(self):
        pass


class Arduino:
    INITIAL_DELAY = 4

    def __init__(self):
        self._serial = None
        self._brightness = 0.25

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = min(1, max(value, 0))

    def start(self):
        for device in glob.glob("/dev/ttyUSB*"):
            print("Trying to connect to %s" % device)
            try:
                self._serial = Serial(device, 115200)
                self._serial.reset_input_buffer()
                self._serial.reset_output_buffer()
                print("Connected to serial port %s" % device)
                sleep(self.INITIAL_DELAY)
                return
            except SerialException:
                pass

        self._serial = DummySerial()
        print("Failed to connect to a serial port.")

    def write_pixels(self, data):
        pixel_bytes = (data * int(255 * self._brightness)).astype(np.uint8).tobytes()
        self._serial.write(pixel_bytes)
