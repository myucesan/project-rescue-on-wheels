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


	'''
	#Toggle backlight on-off-on (implement later on)
	lcd_backlight(True)
	time.sleep(0.5)
	lcd_backlight(False)
	time.sleep(0.5)
	lcd_backlight(True)
	time.sleep(0.5)
	'''

	while True:

		#Send some centred test
		lcd_string("Raspberry Pi", LCD_LINE_1, 2)
		lcd_string("Model B", LCD_LINE_2, 2)

		time.sleep(3) #3 second delay

		#Blank display
		lcd_byte(0x01, LCD_CMD)

		time.sleep(3) #3 second delay

def lcd_init():
	#initialise display
	lcd_byte(0x33, LCD_CMD) # 110011 Initialise
	lcd_byte(0x32, LCD_CMD) # 110010 Initialise
	lcd_byte(0x06, LCD_CMD) #000110 Cursor move direction
	lcd_byte(0x0C, LCD_CMD) #001100 Display On, Cursor Off, Blink Off
	lcd_byte(0x28, LCD_CMD) #101000 Data length, number of lines, font size
	lcd_byte(0x01, LCD_CMD) #000001 Clear display
	time.sleep(E_DELAY)

def lcd_byte(bits, mode):

	#Send byte to data pins
	#bits = data
	#mode = True for character
	#		False for command

	GPIO.output(LCD_RS, mode) #RS

	# High bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x10==0x10:
		GPIO.output(LCD_D4, True)
	if bits&0x20==0x20:
		GPIO.output(LCD_D5, True)
	if bits&0x40==0x40:
		GPIO.output(LCD_D6, True)
	if bits&0x80==0x80:
		GPIO.output(LCD_D7, True)

	#toggle 'Enable' pin
	lcd_toggle_enable()

	#Low bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits & 0x01 == 0x01:
		GPIO.output(LCD_D4, True)
	if bits & 0x02 == 0x02:
		GPIO.output(LCD_D5, True)
	if bits & 0x04 == 0x04:
		GPIO.output(LCD_D6, True)
	if bits & 0x08 == 0x08:
		GPIO.output(LCD_D7, True)

	#Toggle 'Enable' pin
	lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)


def lcd_string(message, line, style):
	# Send string to display
	# style=1 Left justified
	# style=2 Centred
	# style=3 Right justified

	if style == 1:
		message = message.ljust(LCD_WIDTH, " ")
	elif style == 2:
		message = message.center(LCD_WIDTH, " ")
	elif style == 3:
		message = message.rjust(LCD_WIDTH, " ")

	lcd_byte(line, LCD_CMD)

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]), LCD_CHR)


def lcd_backlight(flag):
	# Toggle backlight on-off-on
	GPIO.output(LED_ON, flag)


if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		lcd_byte(0x01, LCD_CMD)
		lcd_string("Goodbye!", LCD_LINE_1, 2)
		GPIO.cleanup()