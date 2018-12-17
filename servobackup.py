import time
import os
from threading import Thread
from timer import *

class Servo:
    
    _PIN = 15
    _MAX = 2500
    _MID_MAX = 2000
    _MID = 1500
    _MID_MIN = 1000
    _MIN = 500
    _start = False
    _timer = None
    
    def __init__(self):
        os.system("sudo service servoblaster stop")
        self._timer = Timer()

    def start(self):
        os.system("sudo service servoblaster start")
        self._start = True


    def set(self, value):
        os.system("echo " + "P1-" + str(self._PIN) + "=" + str(value) + "us > /dev/servoblaster")
      
    def run(self):
        
        while self._start:
            self.set(self._MID_MAX)
            self._timer.pause(0.5)
            self.set(self._MID_MIN)
            self._timer.pause(0.5)

    def stop(self):
        self._start = False
        os.system("sudo service servoblaster stop")

servo = Servo()
servo.start()
servo.run()

