from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import numpy as np

_logger = logging.getLogger(__name__)


class NeoPixels(object):
    LED_COUNT = 256  # Number of LED pixels.
    LED_PIN = 21  # GPIO pin connected to the pixels (must support PWM!). 18=PWM, 21=PCM, 10=SPI-MOSI
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 5  # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    
    def __init__(self):
        from neopixel import Adafruit_NeoPixel as NeoPixel
        
        self._pixels = NeoPixel(num=self.fLED_COUNT,
                                pin=self.LED_PIN,
                                freq_hz=self.LED_FREQ_HZ, 
                                dma=self.LED_DMA,
                                invert=self.LED_INVERT,
                                brightness=self.LED_BRIGHTNESS)
        try:
            self._pixels.begin()
            _logger.info("Initialized NeoPixel OK")
        except RuntimeError:
            _logger.error("Failed to initialize NeoPixels")
            raise

        self._write_pixels(np.zeros((16, 16, 3)))

    def write_pixels(self, data):
        for y, row in enumerate((data * 255).astype(np.uint8)):
            for x, color in enumerate(row):
                self._pixels.setPixelColorRGB(y * 16 + x, *color)
        self._pixels.show()
