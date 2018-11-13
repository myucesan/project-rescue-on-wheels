#!/usr/bin/python
import RPi.GPIO as gpio 
from Bus import * 

class MotorControl():

    def __init__(self):
        self.bus = Bus().get_bus()
	self.MOTOR_ADDRESS = self.bus.get_motor_address()
	#bus._MOTOR_ADDRESS
        #Initializing directions
        self.MotorFD = [7, 3, 0xa5, 2, 3, 0xa5, 2]
        self.MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2]
        self.MotorR = [7, 3, 0xa5, 2, 3, 0xa5, 1]
        self.MotorBD = [7, 3, 0xa5, 1, 3, 0xa5, 1]
        self.MotorST = [7, 0, 0, 0, 0, 0, 0]
        # Motor speed
	#self.MOTOR_ADDRESS = self.bus.
	self.Totalpower = [4, 220]
	self.Softstart = [0x91, 100, 0]

    def set_up(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Totalpower)
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Softstart)

    def forward(self):
        # Drive forward
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorFD)
    
    def backward(self):
        # Drive backward
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorBD)
    def left(self):
        # Drive left-forward
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorL)
    def right(self):
        # Drive right forward
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorR)
    def stop(self):
        # Stop driving
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorST)
    def set_speed(self, speed):
        # Set motor speed
        self.Totalpower[1] = speed
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Totalpower)
        self.bus.write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Softstart)
    def drive(self, direction):
        if direction == "forward":
            self.forward()
        if direction == "right":
            self.right()
        if direction == "left":
            self.left()
        if direction == "backward":
            self.backward()
        if direction == "stop":
            self.stop()
    def reserve_drive(self, direction):
        if direction == "forward":
            self.backward()
        if direction == "right":
            self.left()
        if direction == "left":
            self.right()
        if direction == "backward":
            self.forward()
        if direction == "stop":
            self.stop()
