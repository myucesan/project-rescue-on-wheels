#!/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from threading import *
from curtsies import Input


#vooruit
MotorFD = [7,3,0xa5,2,3,0xa5,2]
MotorFL = [7, 0, 0, 0, 3, 0xa5, 2]
MotorFR = [ 7, 3, 0xa5, 2, 0, 0, 0]
MotorST = [7,0,0,0,0,0,0]
#achteruit
MotorBD = [7,3,0xa5,1,3,0xa5,1]
MotorBL = [7,0,0,0,3,0xa5,1]
MotorBR = [7,3,0xa5,1,0,0,0]

bus = smbus.SMBus(1)
#Adress of the I2C_SLAVE
SLAVE_ADDRESS = 0x32

def Motorinit():
    Totalpower = [4,170]
    Softstart = [0x91,100,0]
    #char *filename = (char*)"/dev/i2c-1";
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, Totalpower)
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, Softstart)

def MotorControl():

    while True:

        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                if e == 'w':
                    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorFD)
                elif e == 'a':
                    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorFL)
                elif e == 'd':
                    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorFR)
                elif e == 's':
                    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorBD)
                elif e == 'f':
                    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorST)
                    break
                elif e == 'e':
                    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorST)





def main():

    thread = Thread(target = MotorControl)
    Motorinit()
    thread.start()
    thread.join()

main()
