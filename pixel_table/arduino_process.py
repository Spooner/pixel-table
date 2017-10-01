import glob
import sys
from time import time, sleep
from multiprocessing import Process, Queue

import numpy as np
from serial import Serial
from serial.serialutil import SerialException


class DummySerial:
    def write(self, data):
        pass

    def read(self):
        sleep(0.001)
        return b"X"

    def reset_input_buffer(self):
        pass


class ArduinoProcess(Process):
    INITIAL_DELAY = 4

    def __init__(self):
        super().__init__()
        self.daemon = True
        self._serial = self._connected_at = None
        self._queue = Queue()

    def _open(self):
        self._connected_at = time()

        for device in glob.glob("/dev/ttyUSB*"):
            print("Trying to connect to %s" % device)
            try:
                self._serial = Serial(device, 115200)
                print("Connected to serial port %s" % device)
                return
            except SerialException:
                pass

        self._serial = DummySerial()
        print("Failed to connect to a serial port.")

    def run(self):
        self._open()
        # self._serial.reset_output_buffer()
        self._serial.reset_input_buffer()

        # Spit out 16*3=48 byte chunks (columns, left to right) that the Arduino can cope with (has a 64-byte buffer).
        while True:
            data = self._queue.get()
            self._write_pixels(data)

    def _write_pixels(self, data):
        if time() < self._connected_at + self.INITIAL_DELAY:
            return

        print("Writing to serial: ", end="", file=sys.stderr)
        for column in data:
            self._write_column(column)
        print(file=sys.stderr)

    def _write_column(self, column):
        column = (column * 255).astype(np.uint8).tobytes()
        try:
            print("c", end='', file=sys.stderr)
            self._serial.write(column)
            print(self._serial.read().decode(), end='', file=sys.stderr)  # Wait for ACK before sending more.
        except (SerialException, AttributeError):
            print("Failed to send serial data.", file=sys.stderr)

    def write_pixels(self, data):
        self._queue.put(data)
