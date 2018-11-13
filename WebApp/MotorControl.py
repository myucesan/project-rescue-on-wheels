# !/usr/bin/python
import RPi.GPIO as gpio
from Bus import *
import time


class MotorControl():

    def __init__(self):
        self.bus = Bus()
        self.MOTOR_ADDRESS = self.bus.get_motor_address()
        # bus._MOTOR_ADDRESS
        # Initializing directions
        self.MotorFD = [7, 3, 0xa5, 2, 3, 0xa5, 2]
        self.MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2]
        self.MotorR = [7, 3, 0xa5, 2, 3, 0xa5, 1]
        self.MotorBD = [7, 3, 0xa5, 1, 3, 0xa5, 1]
        self.MotorST = [7, 0, 0, 0, 0, 0, 0]
        # Motor speed
        # self.MOTOR_ADDRESS = self.bus.
        self.Totalpower = [4, 220]
        self.Softstart = [0x91, 100, 0]
        # state n prevstate
        self.prevDirection = None
        # Time
        self.begin_time = None
        self.end_time = None
        self.time = None

    def set_up(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Totalpower)
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Softstart)

    def forward(self):
        # Drive forward
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorFD)

    def backward(self):
        # Drive backward
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorBD)

    def left(self):
        # Drive left-forward
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorL)

    def right(self):
        # Drive right forward
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorR)

    def stop(self):
        # Stop driving
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.MotorST)

    def set_speed(self, speed):
        # Set motor speed
        self.Totalpower[1] = speed
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Totalpower)
        self.bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self.Softstart)

    def drive(self, direction):
        print("prevDirection")
        print(self.prevDirection)

        if self.begin_time is None:
            self.begin_time = time.time()
        elif direction == "stop":
            self.end_time = time.time()
            self.time = self.end_time - self.begin_time
            print(self.time)
            self.begin_time = None
			# 1. niets 1 seconde ...
			# 2. forward doen voor 10 seconde
			# 3. gaat stop functie in.
			# 4. 5 seconde niets doen
			# 5. forward

			# 1. left 5 seconde 15:45:20
			# 2. forward 5 seconde 15:45:25
        elif self.prevDirection is not None and direction != self.prevDirection:
            self.end_time = time.time()
            self.time = self.end_time - self.begin_time
            print(self.time)
            self.begin_time = time.time()

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

        self.prevDirection = direction

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

