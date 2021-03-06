# Reads analog values and converts it to degrees Celcius.
# Author: Yoshio Schermer
import time
import math
from timer import *
from spi_dev import *
from adc import *

class temperature:

    _timer = None

    def __init__(self):
        # Hardware SPI configuration:
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        self.mcp = adc(spi_dev(self.SPI_PORT, self.SPI_DEVICE))
        self._temperature = None
        self._timer = Timer()

    def convert(self):

        raw = self.mcp.read_adc(0)
        if raw > 0:
            self._temperature = math.log(10000.0 * ((1024.0 / raw - 1)))
            self._temperature = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * self._temperature * self._temperature )) * self._temperature )
            self._temperature = self._temperature - 273.15
            return self._temperature
        else:
            return 0
