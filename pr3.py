#!/usr/bin/python
import smbus
import time
import thread
from threading import *

MotorHF = [7,3,0xa5,2,3,0xa5,2]
MotorST = [7,0,0,0,0,0,0]
MotorHR = [7,3,0xa5,1,3,0xa5,1]

bus = smbus.SMBus(1)
#Adress of the I2C_SLAVE
SLAVE_ADDRESS = 0x32

def Motorinit():
    Totalpower = [4,250]
    Softstart = [0x91,23,0]
    #char *filename = (char*)"/dev/i2c-1";
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, Totalpower)
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, Softstart)

def MotorControl():

    while True:

        #write(fd,&MotorHF[0],7);  //forward
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorHF)
        #usleep(3000000);
        time.sleep(3000)
        #write(fd,&MotorST[0],7);  //stop
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorST)

        #usleep(3000000);
        time.sleep(3000)
        #write(fd,&MotorHR[0],7);  //reverse
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorHR)
        time.sleep(3000)
        #usleep(3000000);

        #write(fd,&MotorST[0],7);   //stop
        bus.write_i2c_block_data(SLAVE_ADDRESS, 0, MotorHF)
        #usleep(2000000);
        time.sleep(2000)

def main():

    thread = Thread(target = MotorControl)
    Motorinit()
    thread.start()
    thread.join()

main()