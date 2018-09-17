#!/bin/bash
# Script to start our application
echo "Doing autorun script ..."

echo "Autorun script sets clockfreq i2c on a low value to avoid clock stretching"

sudo modprobe -r i2c_bcm2708
sudo modprobe  i2c_bcm2708 baudrate=4000

echo "executing  /home/pi/robot/pr  is now turned off"
#turn auto executing on by removing the # sign in the next rule
#sudo /home/pi/row/pr
