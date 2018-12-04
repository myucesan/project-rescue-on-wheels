import smbus
import math


class compass(object):
    __instance = None
    bus = smbus.SMBus(1)
    adr = 0x1e
    north = [0, 20]
    east = [50, 60]
    south = [65500, 65535]
    west = [65495, 65499]

    def get_values(self):
        self.bus.write_byte_data(self.adr, 0x00, 0x70)
        self.bus.write_byte_data(self.adr, 0x01, 0xA0)
        self.bus.write_byte_data(self.adr, 0x02, 0x01)
        xh = self.bus.read_byte_data(self.adr, 0x03)
        xl = self.bus.read_byte_data(self.adr, 0x04)
#        zh = self.bus.read_byte_data(self.adr, 0x05)
#        zl = self.bus.read_byte_data(self.adr, 0x06)
        yh = self.bus.read_byte_data(self.adr, 0x07)
        yl = self.bus.read_byte_data(self.adr, 0x08)

        x = (xh << 8) | xl
        y = (yh << 8) | yl
#        z = (zh << 8) | zl

#        angle = (math.atan2(y, x)) * 180 / math.pi

#        if angle < 0:
#            angle += 360

#        return [x, y]
        return x

    def get_direction(self):
        direction = "North"
        value = int(self.get_value())
        if self.north[0] <= value <= self.north[1]:
            direction = "North"

        elif self.east[0] <= value <= self.east[1]:
            direction = "East"

        elif self.south[0] <= value <= self.south[1]:
            direction = "South"

        elif self.west[0] <= value <= self.west[1]:
            direction = "West"

        return direction
