from MotorControl import *
from LCD import *
from temperature import *
from light import *
from compass import *
from distance import *
import time

class Main(object):
    _instance = None
    _motor_control = None
    _lcd = None
    _temperature = None
    _compass = None
    _light = None
    _list = None
    _disabled = False
    _distance = None

    def __new__(self):
  
        if self._instance is None:
            self._instance = super(Main, self).__new__(self)
            self._motor_control = MotorControl()
            # print(self._motor_control)
            self._lcd = LCD()
            self._lcd.start()
            self._temperature = temperature()
            self._light = light()
            self._distance = Distance()
            self._compass = compass(declination=(1,19))

        return self._instance

    def disable(self):
        self._disabled = True

    def enable(self):
        self._disabled = False

    def is_disabled(self):
        return self._disabled
