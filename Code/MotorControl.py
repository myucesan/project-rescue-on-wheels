#!/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from threading import * #Wordt nog gebruikt

 class MotorControl:

     def __init__(self):
         #bus initialization
         self.bus = smbus.SMBus(1)
         #Motor direction
         self.MotorFD = [7,3,0xa5,2,3,0xa5,2]
         self.MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2]
         self.MotorR = [ 7, 3, 0xa5, 2, 3, 0xa5, 1]
         self.MotorST = [7,0,0,0,0,0,0]
         #Motor speed
         self.Totalpower = [4,220]
         self.Softstart = [0x91,100,0]
         #Address to access motor
         self.SLAVE_ADDRESS = 0x32
         #pin set up for resistor
         gpio.setmode(gpio.BCM)
         gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
         #Writing totalpower and softstart to bus
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.Totalpower)
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.Softstart)


     def forward(self):
         #Drive forward
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.MotorFD)

     def backward(self):
         #Drive backward
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.MotorBD)

     def left(self):
         #Drive left-forward
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.MotorL)

     def right(self):
         #Drive right forward
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.MotorR)

    def stop(self):
        #Stop driving
        self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.MotorST)

    def setSpeed(self, speed):
        #Set motor speed
        self.Totalpower[1] = speed
	    self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.Totalpower)
