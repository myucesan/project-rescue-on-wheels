#!/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from threading import *

bus = smbus.SMBus(1)
#Adress of the I2C_SLAVE
SLAVE_ADDRESS = 0x70
cmMeasure = [00, 0x51] #command for measurement in cm
readLowByte = [0x03]
lowByte = 3

def main():
    time.sleep(1)
    while True:
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, cmMeasure)
        time.sleep(1)
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, readLowByte)
        low = bus.read_byte_data(SLAVE_ADDRESS, 0)
        print(low)
        time.sleep(2)

main()