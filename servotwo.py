import RPi.GPIO as GPIO
import time
from threading import Thread

class Servo:

    _control = [5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
    _PIN = 11
    _pwm = None
    _start = True

    def __init__(self, hz):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._PIN,GPIO.OUT)
        self._pwm = GPIO.PWM(self._PIN, hz)
        self._pwm.start(2.5)

    def __reset(self):
        self._pwm.ChangeDutyCycle(2.5)

    def start(self):
        while self._start:
            for x in range(11):
                self._pwm.ChangeDutyCycle(self._control[x])
                time.sleep(0.02)


            for x in range(9,0,-1):
                self._pwm.ChangeDutyCycle(self._control[x])
                time.sleep(0.02)
    def stop(self):
        self._start = False

