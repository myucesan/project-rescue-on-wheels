from MotorControl import *
from LCD import *
from temperature import *
from light import *
from magneto import *
import time


class Main(object):
    _instance = None
    _motor_control = None
    _lcd = None
    _temperature = None
    _compass = None
    _light = None
    _list = None

    def __new__(self):
  
        if self._instance is None:
            self._instance = super(Main, self).__new__(self)
            self._motor_control = MotorControl()
            # print(self._motor_control)
            self._lcd = LCD()
            self._lcd.start()
            self._temperature = temperature()
            self._light = light()
            self._compass = Compass()
            print(self._compass)
        return self._instance

