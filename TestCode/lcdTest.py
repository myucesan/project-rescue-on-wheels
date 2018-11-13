#The wiring for the LCD is as follows:
#1 : GND
#2 : 5V
#3 : Contrast (0-5v - connect to ground for max, potentio for adjustment)
#4 : RS (register select -  Low == Commands for the LCD, High == Data mode)
#5 : R/W (Read/Write - Connect to ground for write only)
#6 : Enable signal (Toggle to write data to registers)
#7 : Data bit 0 - NOT USED
#8 : Data bit 1 - NOT USED
#9 : Data bit 2 - NOT USED
#10 : Data bit 3 - NOT USED
#11 : Data bit 4
#12 : Data bit 5
#13 : Data bit 6
#14 : Data bit 7
#15 : LCD backlight VDD (5v)
#16 : LCD backlight GND

#import
import RPi.GPIO as GPIO
import time

#Define GPIO to LCD mapping
LCD_RS = 7
LCD_E = 15
LCD_D4 = 29
LCD_D5 = 25
LCD_D6 = 24
LCD_D7 = 23
#LED_ON =  #Connect this to backlight pin to make the backlight toggle-able

#Define some device constants
LCD_WIDTH = 16 #max chars per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 #LCD RAM address line 1
LCD_LINE_2 = 0xC0 #LCD RAM address line 2

#Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
	#main program block

	GPIO.setmode(GPIO.BCM) #Use BMC GPIO numbers
	GPIO.setup(LCD_E, GPIO.OUT) # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
#	GPIO.setup(LED_ON, GPIO.OUT) #backlight enable

	#Initialise display
	lcd_init()

	#Toggle backlight on-off-on
	lcd_backlight(true)

