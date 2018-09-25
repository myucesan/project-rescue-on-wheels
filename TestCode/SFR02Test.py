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


def main():
    time.sleep(1)
    while True:
        print("hi")
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, cmMeasure)
        time.sleep(1)
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, readLowByte)
        low = read_byte_data(readLowByte, 0)
        print(low)
        time.sleep(2)

main()