import smbus
import time

class Bus:
   
    _bus = None
    _MOTOR_ADDRESS = None
    _MAGNETO_ADDRESS = None
    _DISTANCE_ADDRESS = None

    def __init__(self):
        self._bus = smbus.SMBus(1)
        time.sleep(2)
        self._MOTOR_ADDRESS = 0x32
        self._DISTANCE_ADDRESS = 0x70

    def get_motor_address(self):
        return self._MOTOR_ADDRESS
  
    def get_distance_address(self):
        return self._DISTANCE_ADDRESS
	
    def get_bus(self):
        return self._bus

