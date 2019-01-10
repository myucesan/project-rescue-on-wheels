import RPi.GPIO as GPIO
import time
from threading import Thread

class Servo:

    _control = [5,5.5,6,6.5,7,7.5,8,8.5,9]
    _PIN = 15
    _pwm = None
    _start = False

    def __init__(self, hz):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._PIN,GPIO.OUT)
        self._pwm = GPIO.PWM(self._PIN, hz)
        #self._pwm.start(2.5)

    def __reset(self):
        self._pwm.ChangeDutyCycle(1)

    def start(self):
       # self._pwm.ChangeDutyCycle(9)
        self._start = True
        while self._start:
            for x in range(9):
                self._pwm.ChangeDutyCycle(self._control[x])
                time.sleep(0.05)
                print(self._control[x])


            for x in range(7,0,-1):
                self._pwm.ChangeDutyCycle(self._control[x])
                time.sleep(0.05)
                print(self._control[x])

    def stop(self):
        self._start = False

    def prepare(self):
        self._pwm.start(2.5)

#Servo(50).start()
