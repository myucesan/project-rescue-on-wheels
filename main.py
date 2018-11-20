from MotorControl import *
from LCD import *
import time

class Main(object):

	_instance = None
	_motor_control = None
	_lcd = None

	def __new__(self):
		print("test")
		if self._instance is None:
			self._instance = super(Main,self).__new__(self)
			self._motor_control = MotorControl()
			self._lcd = LCD()
			self._lcd.start()

		return self._instance

