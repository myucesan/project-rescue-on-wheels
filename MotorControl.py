# !/usr/bin/python
import RPi.GPIO as gpio
from Bus import *
import time


class MotorControl:

    _bus = None
    _MOTOR_ADDRESS = None
    _MotorFD = [7, 3, 0xa5, 2, 3, 0xa5, 2]
    _MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2]
    _MotorR = [7, 3, 0xa5, 2, 3, 0xa5, 1]
    _MotorBD = [7, 3, 0xa5, 1, 3, 0xa5, 1]
    _MotorST = [7, 0, 0, 0, 0, 0, 0]
    _Totalpower = [4, 220]
    _Softstart = [0x91, 100, 0]
    _prevDirection = None
    _begin_time = None
    _end_time = None
    _time = None

    def __init__(self):
        self._bus = Bus()
        self._MOTOR_ADDRESS = self._bus.get_motor_address()


    def set_up(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._Totalpower)
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._Softstart)

    def forward(self):
        # Drive forward
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._MotorFD)

    def backward(self):
        # Drive backward
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._MotorBD)

    def left(self):
        # Drive left-forward
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._MotorL)

    def right(self):
        # Drive right forward
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._MotorR)

    def stop(self):
        # Stop driving
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._MotorST)

    def set_speed(self, speed):
        # Set motor speed
        self._Totalpower[1] = speed
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._Totalpower)
        self._bus.get_bus().write_i2c_block_data(self._MOTOR_ADDRESS, 0, self._Softstart)

    def drive(self, direction):

        if self._begin_time is None:
            self._begin_time = time.time()
        elif direction == "stop":
            self._end_time = time.time()
            self._time = self._end_time - self._begin_time
            self._begin_time = None
        elif self._prevDirection is not None and direction != self._prevDirection:
            self._end_time = time.time()
            self._time = self._end_time - self._begin_time
            self._begin_time = time.time()

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

        self._prevDirection = direction

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

