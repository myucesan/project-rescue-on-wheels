import time
import os
from threading import Thread

class Servo:
    
    _PIN = 15
    _MAX = 2500
    _MID_MAX = 2000
    _MID = 1500
    _MID_MIN = 1000
    _MIN = 500
    _start = True

    def set(self, value):
        os.system("echo " + "P1-" + str(self._PIN) + "=" + str(value) + "us > /dev/servoblaster")
      
    def run(self):
        os.system("sudo service servoblaster start")
        while self._start:
            self.set(self._MID_MAX)
            time.sleep(1)
            self.set(self._MID_MIN)
            time.sleep(1)

    def stop(self):
        self._start = False
        os.system("sudo service servoblaster stop")


