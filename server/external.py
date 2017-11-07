from __future__ import absolute_import, division, print_function, unicode_literals

import glob
from time import sleep
import logging

import numpy as np
from serial import Serial
from serial.serialutil import SerialException
import smbus2

_logger = logging.getLogger(__name__)

READY_CHAR = b'R'


class MockSerial(object):
    def write(self, data):
        sleep(0.05)

    def read(self):
        sleep(0.05)
        return READY_CHAR

    def setDTR(self, value):
        pass


class MockBus(object):
    def write_byte_data(self, i2c_addr, register, value):
        sleep(0.00001)


class External(object):
    SERIAL_SPEED = 115200
    DEVICE_BUS = 1
    ARDUINO_ADDRESS, ARDUINO_REGISTER = 0x15, 0x00
    TOUCH_ADDRESS, TOUCH_REGISTER = 0x50, 0x00

    def __init__(self):
        self._serial = self._open_serial()
        self._bus = self._open_bus()
        self.reset_serial()

    def _open_serial(self):
        for device in glob.glob("/dev/ttyUSB*"):
            _logger.info("Trying to connect to %s" % device)
            try:
                serial = Serial(device, self.SERIAL_SPEED)
                _logger.info("Connected to serial port: %s" % device)
                return serial
            except SerialException:
                pass

        _logger.warning("Failed to connect to a serial port.")
        return MockSerial()

    def _open_bus(self):
        try:
            bus = smbus2.SMBus(self.DEVICE_BUS)
            _logger.info("Connected to i2c %s" % self.DEVICE_BUS)
        except OSError:
            bus = MockBus()
            _logger.warning("Failed to connect to i2c bus: %s" % self.DEVICE_BUS)

        return bus

    def reset_serial(self):
        """Reset Serial connection"""
        self._serial.setDTR(False)
        sleep(0.022)
        self._serial.setDTR(True)

    def write_pixels(self, data):
        pixel_bytes = (data * 255).astype(np.uint8).tobytes()
        for byte in pixel_bytes:
            self._bus.write_byte_data(self.ARDUINO_ADDRESS, self.ARDUINO_REGISTER, byte)
