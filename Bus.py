import smbus

class Bus:
   
    _bus = None
    _MOTOR_ADDRESS = None

    def __init__(self):
        self._bus = smbus.SMBus(1)
        self._MOTOR_ADDRESS = 0x32

    def get_motor_address(self):
        return self._MOTOR_ADDRESS
	
    def get_bus(self):
        return self._bus

