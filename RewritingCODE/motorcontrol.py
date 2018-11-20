#!/usr/bin/python
import RPi.GPIO as gpio
from bus import *

class MotorControl:
    _bus = None
    _MotorFD = None
    _MotorL = None
    _MotorR = None
    _MotorBD = None
    _MotorST = None
    _Totalpower = None
    _Softstart = None
    def __init__(self):
        self._bus = Bus()
        #Initializing directions
        self._MotorFD = [7, 3, 0xa5, 2, 3, 0xa5, 2]
        self._MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2]
        self._MotorR = [7, 3, 0xa5, 2, 3, 0xa5, 1]
        self._MotorBD = [7, 3, 0xa5, 1, 3, 0xa5, 1]
        self._MotorST = [7, 0, 0, 0, 0, 0, 0]
        # Motor speed
        self._Totalpower = [4, 220]
        self._Softstart = [0x91, 100, 0]

    def set_up(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._Totalpower)
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._Softstart)

    def forward(self):
        # Drive forward
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._MotorFD)

    def backward(self):
        # Drive backward
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._MotorBD)

    def left(self):
        # Drive left-forward
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._MotorL)

    def right(self):
        # Drive right forward
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._MotorR)

    def stop(self):
        # Stop driving
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._MotorST)

    def set_speed(self, speed):
        # Set motor speed
        self.Totalpower[1] = speed
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._Totalpower)
        self._bus.get_bus().write_i2c_block_data(self.MOTOR_ADDRESS, 0, self._Softstart)

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
