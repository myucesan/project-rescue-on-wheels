# !/usr/bin/python
import RPi.GPIO as gpio
from Bus import *
import time
from stopwatch import *
from magneto2 import *

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
    _timer = None
    _list = None
    _magneto = None

    def __init__(self):
        self._bus = Bus()
        self._MOTOR_ADDRESS = self._bus.get_motor_address()
        self._timer = Stopwatch()
        self._list = []
        self._magneto = Compass()

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

        if self._timer._start is None:
            self._timer.start()
        elif direction == "stop":
            self._list.append({"direction": self._prevDirection, "time": self._timer.stop()})
            print(self._prevDirection)
        elif self._prevDirection is not None and direction != self._prevDirection:
            self._list.append({"direction": self._prevDirection, "time": self._timer.stop()})
            print(self._prevDirection)
            self._timer.start()

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

    def reverse_drive(self):

        for i in reversed(self._list):

            if i['direction'] == "forward":
                self.backward()
            if i['direction'] == "right":
                self.left()
            if i['direction'] == "left":
                self.right()
            if i['direction'] == "backward":
                self.forward()
            if i['direction'] == "stop":
                self.stop()
            self._timer.pause(i['time'])

        self.stop()
        self._list.clear()

