#!/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from threading import *

class srf02:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        #Adress of the I2C_SLAVE
        self.SLAVE_ADDRESS = 0x70
        self.cmMeasure = 81 #command for measurement in cm
        #readLowByte = [0x03]
        #self.lowByte = 3

    def calculateDistance(self):
        while True:
            self.bus.write_byte_data(self.SLAVE_ADDRESS, 0 ,self.cmMeasure)
            time.sleep(1)
            distanceHigh = self.bus.read_word_data(self.SLAVE_ADDRESS, 2) #/ 255
            distanceLow = self.bus.read_word_data(self.SLAVE_ADDRESS, 3) #/ 255
            minDistanceHigh = self.bus.read_word_data(self.SLAVE_ADDRESS, 4) #/ 255
            minDistanceLow = self.bus.read_word_data(self.SLAVE_ADDRESS, 5) #/ 255
            print("High Distance: " + distanceHigh + "Low Distance: " + distanceLow)
            print("Minimal high Distance:" + minDistanceHigh + "Minimal low Distance: " + minDistanceLow)
            time.sleep(2)

            #bus.write_i2c_block_data(SLAVE_ADDRESS, 0, readLowByte)
            #low = bus.read_byte_data(SLAVE_ADDRESS, 0)
            #print(low)
            #time.sleep(1)

srf02().calculateDistance()

