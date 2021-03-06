import smbus
import math
import time

class compass(object):
    __instance = None
    bus = smbus.SMBus(1)
    adr = 0x1e # Address of compass
    north = [0, 20] # value range for north
    east = [50, 60] # value range for east
    south = [65500, 65535] # value range for south
    west = [65495, 65499] # value range for west

    def get_values(self):
        self.bus.write_byte_data(self.adr, 0x00, 0x70)
        self.bus.write_byte_data(self.adr, 0x01, 0xA0)
        self.bus.write_byte_data(self.adr, 0x02, 0x01)
        xh = self.bus.read_byte_data(self.adr, 0x03)
        xl = self.bus.read_byte_data(self.adr, 0x04)
        zh = self.bus.read_byte_data(self.adr, 0x05)
        zl = self.bus.read_byte_data(self.adr, 0x06)
        yh = self.bus.read_byte_data(self.adr, 0x07)
        yl = self.bus.read_byte_data(self.adr, 0x08)

        x = (xh << 8) | xl # high bit low bit 
        y = (yh << 8) | yl
#        z = (zh << 8) | zl

        angle = math.atan2(y, x) * 180 / math.pi + 180 # formule hoek

        if angle < 0:
            angle += 360 # works with negative values but this corrects it

#        return [x, y]
        return angle

    def get_direction(self):
        direction = "North"
        value = int(self.get_values())
        if self.north[0] <= value <= self.north[1]:
            direction = "North"

        elif self.east[0] <= value <= self.east[1]:
            direction = "East"

        elif self.south[0] <= value <= self.south[1]:
            direction = "South"

        elif self.west[0] <= value <= self.west[1]:
            direction = "West"
        print(value)
        return direction

comp = compass()
while True:
    print(comp.get_values())
    time.sleep(1)
