import glob
import sys
from time import time
from multiprocessing import Process, Queue

import numpy as np
from serial import Serial
from serial.serialutil import SerialException


class ArduinoProcess(Process):
    INITIAL_DELAY = 4

    def __init__(self):
        super().__init__()
        self._serial = self._connected_at = None
        self._queue = Queue()

    def _open(self):
        for device in glob.glob("/dev/ttyUSB*"):
            print("Trying to connect to %s" % device)
            try:
                self._serial = Serial(device, 115200)
                self._serial.reset_output_buffer()
                self._serial.reset_input_buffer()
                self._connected_at = time()
                print("Connected to serial port %s" % device)
                return
            except SerialException:
                pass

        print("Failed to connect to a serial port.")

    def run(self):
        self._open()

        # Spit out 16*3=48 byte chunks (columns, left to right) that the Arduino can cope with (has a 64-byte buffer).
        while True:
            data = self._queue.get()
            if self._serial is not None and time() < self._connected_at + self.INITIAL_DELAY:
                continue

            print("Writing to serial: ", end="", file=sys.stderr)
            for column in data:
                self._write_column(column)
            print(file=sys.stderr)

    def _write_column(self, column):
        column = (column * 255).astype(np.uint8).tobytes()
        try:
            self._serial.write(column)
            print(self._serial.read().decode(), end='', file=sys.stderr)  # Wait for ACK before sending more.
        except (SerialException, AttributeError):
            pass #  print("Failed to send serial data.")

    def write_pixels(self, data):
        self._queue.put(data)
