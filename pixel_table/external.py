from __future__ import absolute_import, division, print_function, unicode_literals

import glob
from time import sleep
import logging

import numpy as np
from serial import Serial
from serial.serialutil import SerialException
from Adafruit_MPR121.MPR121 import MPR121
from bitarray import bitarray
import smokesignal

try:
    from neopixel import Adafruit_NeoPixel as NeoPixel, Color
except ImportError:
    class NeoPixel(object):
        def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False,
                     brightness=255, channel=0, strip_type=0):
            self._num = num

        def begin(self):
            pass

        def setPixelColor(self, index, color):
            assert 0 <= index < self._num
            assert isinstance(color, Color)

        def show(self):
            pass

    class Color(object):
        def __init__(self, r, g, b):
            pass

_logger = logging.getLogger(__name__)

READY_CHAR = b'R'

# Capacitive touch
IRQ_PIN = 26
NUM_TOUCHES = 12

# NeoPixels
LED_COUNT = 256  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)


class MockSerial(object):
    def write(self, data):
        sleep(0.05)

    def read(self):
        sleep(0.05)
        return READY_CHAR

    def setDTR(self, value):
        pass


class MockCapTouch(object):
    def __init__(self):
        pass

    def touched(self):
        import random
        return random.choice([0b001000100000, 0b000000100000, 0b000000000000])


class External(object):
    SERIAL_SPEED = 9600
    PLAYER_AND_BUTTON_FOR_TOUCH = {
        0: (0, 0),
        1: (0, 1),
        2: (0, 2),
        3: (1, 0),
        4: (1, 1),
        5: (1, 2),
        6: (2, 0),
        7: (2, 1),
        8: (2, 2),
        9: (3, 0),
        10: (3, 1),
        11: (3, 2),
    }

    def __init__(self):
        self._serial = self._open_serial()
        self.reset_serial()

        self._touches = bitarray(NUM_TOUCHES)
        self._cap_touch = self._open_cap_touch()

        self._pixels = self._open_pixels()

    def _open_cap_touch(self):
        cap_touch = MPR121()
        try:
            if cap_touch.begin():
                cap_touch.touched()  # Just clear out any current changes.
                print("Capacitive touch system engaged")
            else:
                raise RuntimeError
        except RuntimeError:
            print("Capacitive touch system failed")
            cap_touch = MockCapTouch()

        return cap_touch

    def _open_pixels(self):
        pixels = NeoPixel(num=LED_COUNT, pin=LED_PIN, freq_hz=LED_FREQ_HZ, dma=LED_DMA, invert=LED_INVERT,
                          brightness=LED_BRIGHTNESS)
        pixels.begin()

        for i in range(LED_COUNT):
            pixels.setPixelColor(i, Color(0, 0, 0))
        pixels.show()
        return pixels

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

    def reset_serial(self):
        """Reset Serial connection"""
        self._serial.setDTR(False)
        sleep(0.022)
        self._serial.setDTR(True)

    def write_pixels(self, data):
        for y, row in enumerate((data * 255).astype(np.uint8)):
            for x, color in enumerate(row):
                self._pixels.setPixelColor(y * 16 + x, Color(*color))
        self._pixels.show()

    def emit_touch_events(self, dt):
        touches = bitarray(NUM_TOUCHES)
        cap_touches = self._cap_touch.touched()
        for i in range(NUM_TOUCHES):
            touched = cap_touches & (1 << i)
            touches[i] = touched

            player, button = self.PLAYER_AND_BUTTON_FOR_TOUCH[i]
            if touched and not self._touches[i]:
                smokesignal.emit("touch_button_press", player, button)

            if touched:
                smokesignal.emit("touch_button_held", player, button, dt)

            if not touched and self._touches[i]:
                smokesignal.emit("touch_button_release", player, button)

        self._touches = touches
