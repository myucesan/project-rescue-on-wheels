#!/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from Socket import *

class MotorInitialization:

    def __init__(self):
         #bus initialization
         self.bus = smbus.SMBus(1)
         #Motor direction
         self.MotorFD = [7,3,0xa5,2,3,0xa5,2]
         self.MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2]
         self.MotorR = [ 7, 3, 0xa5, 2, 3, 0xa5, 1]
	 self.MotorBD = [7, 3, 0xa5, 1, 3, 0xa5, 1]
         self.MotorST = [7,0,0,0,0,0,0]
         #Motor speed
         self.Totalpower = [4,220]
         self.Softstart = [0x91,100,0]
         #Address to access motor
         self.SLAVE_ADDRESS = 0x32
	 self.prevValue = None
	 self.prevSpeed = None
	 self.socket = Socket()
	 self.state = None
	 self.couchstate = None

    def setUp(self):
	gpio.setmode(gpio.BCM)
	gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
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
	 print(self.Totalpower[1])
	 time.sleep(1)	
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.Totalpower)
         self.bus.write_i2c_block_data(self.SLAVE_ADDRESS, 0, self.Softstart)

    def drive(self):
	
    	while True:
        	self.socket.receiveValues()
		try:
			if self.socket.backtrack == 0:
				self.state = self.socket.state
	        		if self.prevValue == None or self.prevValue != self.state:
					self.prevValue = self.state
                			self.state = self.socket.state
			else:
				self.state = "stop"
				for doc in range(self.socket.docCounter):
					openedDoc = self.socket.repo.openDoc(doc+1)
					if openedDoc["state"] == "forward":
						self.backward()
					if openedDoc["state"] == "right":
						self.left()
					if openedDoc["state"] == "left":
						self.right()
					if openedDoc["state"] == "backward":
						self.forward()
					time.sleep(openedDoc["time"])
				self.stop()
				for doc in self.socket.repo:
					del doc
							
                        if self.state == "forward":
                        	self.forward()
                        if self.state == "right":
                        	self.right()
                        if self.state == "left":
                        	self.left()
                        if self.state == "backward":
                        	self.backward()
                        if self.state == "stop":
            	        	self.stop()
		except:
			self.socket.close()
		#if self.prevSpeed == None or self.prevSpeed != self.socket.speed:
			#self.setSpeed(self.socket.speed)
