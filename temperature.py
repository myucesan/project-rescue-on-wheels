# Simple example of reading the MCP3008 analog input channels and 
# printing them all out. Author: Tony DiCola License: Public Domain
import time
import math

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class temperature:
	def __init__(self):
		# Hardware SPI configuration:
		self.SPI_PORT = 0
		self.SPI_DEVICE = 0
		self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))
		self._temperature = None

	def convert(self):
		raw = self.mcp.read_adc(0)
		print(raw)
		if raw > 0:
			self._temperature = math.log(10000.0 * ((1024.0 / raw - 1)))
			self._temperature = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * self._temperature * self._temperature )) * self._temperature )
			self._temperature = self._temperature - 273.15
			return self._temperature
		else:
			return 0
