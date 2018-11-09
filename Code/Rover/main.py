import sys
from Socket import *
from MotorInitialization import *
from threading import *
MotorInitialization = MotorInitialization()

def main():
	print("main invoked")
	thread = Thread(target=MotorInitialization.drive())
	MotorInitialization.setUp()
	thread.start()
	thread.join()

main()
