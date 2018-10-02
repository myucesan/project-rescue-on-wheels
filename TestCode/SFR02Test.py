#!/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from threading import *

class srf02:
    def _init_(self):
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
            distance = self.bus.read_word_data(self.SLAVE_ADDRESS, 2) / 255
            mindistance = self.bus.read_word_data(self.SLAVE_ADDRESS, 4) / 255
            print(distance + " -  Minimal Distance:" + mindistance)
            time.sleep(2)
    
            #bus.write_i2c_block_data(SLAVE_ADDRESS, 0, readLowByte)
            #low = bus.read_byte_data(SLAVE_ADDRESS, 0)
            #print(low)
            #time.sleep(1)

srf02().calculateDistance()

