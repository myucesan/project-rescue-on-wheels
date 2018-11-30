#!/usr/bin/python3

# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import math
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import time
import threading

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

class light:
        def __init__(self):
                # Pin configuration
                self.INPUT_PIN = 18
                self.LDR_THRESHOLD = 200
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                GPIO.setup(self.INPUT_PIN, GPIO.OUT)

                self._light = None

        def start(self):
                while(True):
                        if mcp.read_adc(1) > self.LDR_THRESHOLD:
                                GPIO.output(self.INPUT_PIN,GPIO.HIGH)
                        else:
                                GPIO.output(self.INPUT_PIN,GPIO.LOW)
                        time.sleep(1)

t=threading.Thread(target=light().start).start()
