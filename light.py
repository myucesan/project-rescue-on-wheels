#!/usr/bin/python3
import math
from timer import *
import threading
import RPi.GPIO as GPIO
from adc import *
from spi_dev import *

# Hardware SPI configuration:
class light:

        _timer = None

        def __init__(self):
                self.SPI_PORT   = 0
                self.SPI_DEVICE = 0
                self.mcp = adc(spi_dev(self.SPI_PORT, self.SPI_DEVICE))

                # Pin configuration
                self.INPUT_PIN = 18
                self.LDR_THRESHOLD = 200
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                GPIO.setup(self.INPUT_PIN, GPIO.OUT)
                self._timer = Timer()
                self._light = None

        def start(self):
                while(True):
                        if self.mcp.read_adc(1) > self.LDR_THRESHOLD:
                                GPIO.output(self.INPUT_PIN,GPIO.HIGH)
                        else:
                                GPIO.output(self.INPUT_PIN,GPIO.LOW)
                        self._timer.pause(1)

t=threading.Thread(target=light().start).start()
