import smbus

class Bus:

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.MOTOR_ADDRESS = 0x32
