from __future__ import absolute_import, division, print_function, unicode_literals

from time import sleep
import logging

from serial import Serial
from serial.serialutil import SerialException


_logger = logging.getLogger(__name__)

READY = b"R"


class MockSerial(object):
    def write(self, data):
        sleep(0.01)

    def read(self, size=1):
        return READY

    def readline(self):
        return b"100.9;1234.72;12.99;40.12;12.99;0.0;200.20;100.0;12.99;12.0;24.99;122.2;90.0;12.9;1.0;981.0;"

    def setDTR(self, value):
        pass


class Arduino(object):
    DEVICE = "/dev/ttyAMA0"
    AUDIO_BUCKETS_COMMAND = "F"
    SERIAL_SPEED = 115200
    NUM_AUDIO_BUCKETS = 16
    AUDIO_BUCKETS_FORMAT = "B" * NUM_AUDIO_BUCKETS

    def __init__(self):
        self._serial = self._open()
        self.reset_serial()

    def _open(self):
        _logger.info("Trying to connect to %s" % self.DEVICE)
        try:
            serial = Serial(self.DEVICE, self.SERIAL_SPEED)
            _logger.info("Connected to serial port.")
            assert self._serial.read() == READY
            _logger.info("Received ready response on Serial port.")
            return serial
        except SerialException:
            pass

        _logger.warning("Failed to connect to a serial port.")
        return MockSerial()

    def reset_serial(self):
        """Reset Serial connection"""
        self._serial.setDTR(False)
        sleep(0.022)
        self._serial.setDTR(True)

    def get_fft_buckets(self):
        self._serial.write(self.AUDIO_BUCKETS_COMMAND)
        buckets = [float(n) for n in ";".split(self._serial.readline(self.NUM_AUDIO_BUCKETS))[:-1]]
        return buckets
