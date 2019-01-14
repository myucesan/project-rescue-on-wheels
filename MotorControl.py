# !/usr/bin/python
import RPi.GPIO as gpio
from Bus import *
import time
from timer import *
from distance import *
#from magneto2 import *
from servo import *
from threading import Thread

class MotorControl:
    _bus = None # placeholder for the Bus object, representing smbus
    _MOTOR_ADDRESS = None # Variable representing the address of the motor control board
    _MotorBD = [7, 3, 0xa5, 2, 3, 0xa5, 2]# Array representing the motors going backward
    _MotorL = [7, 3, 0xa5, 1, 3, 0xa5, 2] # Array representing the motors making a left turn: left (motor)wheels are going backward and right (motor)wheels backward
    _MotorR = [7, 3, 0xa5, 2, 3, 0xa5, 1] # Array representing the motors making a right turn: right (motor)wheels are going forward and left (motor)wheels backward
    _MotorFD = [7, 3, 0xa5, 1, 3, 0xa5, 1] # Array representing the motors going forward
    _MotorST = [7, 0, 0, 0, 0, 0, 0] # Array representing the motors stopping
    _Totalpower = [4, 220] # representing motor speed
    _Softstart = [0x91, 100, 0]  # speed the motors slowly build up to
    _prevDirection = None # variable storing the last direction the rover went used for backtracking
    _timer = None # placeholder for the timer object
    _list = None # placeholder for an array
    _distance = None # placeholder for the distance object representing the distance sensor
    _servo = None # placeholder for the servo object representing the servomotor

    def __init__(self): # method that inializes placeholder variables
        self._bus = Bus()
        self._MOTOR_ADDRESS = self._bus.get_motor_address()
        self._timer = Timer()
        self._distance = Distance()
        self._list = []
        self._servo = Servo(50) # parameter in hertz

    def set_up(self):
        gpio.setmode(gpio.BCM) # Sets the GPIO numbering mode to BCM
        gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN) # sets up pin 17 BCM to be an input in pull_up_down resistor mode
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

    # the method used for backtracking, used by reverse_drive()
    def reverse(self):

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

            # checks if interrupt is neccesary (neccesary when obstacle is detected), it stops the rover then
            self._timer.conditional_pause(i['time'], 20, self._distance.get_distance(), [20, 40])
            self.stop()
            self._timer.pause(1)
            #self.stop()
        
        # empties the route that the rover took for a new backtracking after the backtracking button is clicked.
        self._list.clear()
        print(self._list)

    # method called when the backtracking button is clicked
    # check if list has any values and then performs backtracking using threads
    def reverse_drive(self):
        
        if self._list:
            self._servo.prepare()
            self._timer.pause(0.5)
            thread = Thread(target = self.reverse)
            thread1 = Thread(target = self._servo.start)
            thread2 = Thread(target = self._servo.stop)
            thread.start()
            thread1.start()
            thread.join()
            thread2.start()

