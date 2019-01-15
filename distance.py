# Take readings from the I2C SRF02 Ultrasound range sensor

import smbus,time,datetime
from MotorControl import*
from timer import *
from Bus import *

class Distance:
  
  _timer = None
  _bus = None

  def __init__(self):
    self._bus = Bus()
    self._timer = Timer()
  
  def get_distance(self):
    self._bus.get_bus().write_byte_data(self._bus.get_distance_address(), 0, 81)
    distance = self._bus.get_bus().read_word_data(self._bus.get_distance_address(), 2) / 255
    return distance

#dist=Distance()
#while True:
#    print(dist.get_distance())
#    time.sleep(1)
