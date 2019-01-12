# !/usr/bin/python

import RPi.GPIO as GPIO
import time


class LCD:
    # Below variables corresponding to the LCD pins
    _LCD_RS = None # signal for selecting registers
    _LCD_E = None
    _LCD_D4 = None
    _LCD_D5 = None
    _LCD_D6 = None
    _LCD_D7 = None

    _LCD_WIDTH = None
    _LCD_CHR = None
    _LCD_CMD = None

    _LCD_LINE_1 = None
    _LCD_LINE_2 = None

    _E_PULSE = None
    _E_DELAY = None

    _DICT = None
    
    #Initialising variables
    def __init__(self):

        self._LCD_RS = 7
        self._LCD_E = 8
        self._LCD_D4 = 40
        self._LCD_D5 = 37
        self._LCD_D6 = 35
        self._LCD_D7 = 33

        self._LCD_WIDTH = 16
        self._LCD_CHR = True
        self._LCD_CMD = False

        self._LCD_LINE_1 = 0x80
        self._LCD_LINE_2 = 0xC0

        self._E_PULSE = 0.0005
        self._E_DELAY = 0.0005
        
        # Variable representing the first and second line of the LCD
        self._DICT = {self._LCD_LINE_1: None, self._LCD_LINE_2: None}

        # Sets numbering mode to BOARD and setting corresponding pins to output.
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._LCD_E, GPIO.OUT)
        GPIO.setup(self._LCD_RS, GPIO.OUT)
        GPIO.setup(self._LCD_D4, GPIO.OUT)
        GPIO.setup(self._LCD_D5, GPIO.OUT)
        GPIO.setup(self._LCD_D6, GPIO.OUT)
        GPIO.setup(self._LCD_D7, GPIO.OUT)

    # Enables or disables a bit based based on the bits that are given in hexadecimal
    def lcd_byte(self, bits, mode):
        GPIO.output(self._LCD_RS, mode)

        GPIO.output(self._LCD_D4, False)
        GPIO.output(self._LCD_D5, False)
        GPIO.output(self._LCD_D6, False)
        GPIO.output(self._LCD_D7, False)

        if bits & 0x10 == 0x10:
            GPIO.output(self._LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self._LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self._LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self._LCD_D7, True)

        # toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self._LCD_D4, False)
        GPIO.output(self._LCD_D5, False)
        GPIO.output(self._LCD_D6, False)
        GPIO.output(self._LCD_D7, False)

        if bits & 0x01 == 0x01:
            GPIO.output(self._LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self._LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self._LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self._LCD_D7, True)

            # Toggle 'Enable' pin
        self.lcd_toggle_enable()
    
    def lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(self._E_DELAY)
        GPIO.output(self._LCD_E, True)
        time.sleep(self._E_PULSE)
        GPIO.output(self._LCD_E, False)
        time.sleep(self._E_DELAY)
    #clears lcd
    def clear_string(self):
        self.lcd_byte(0x01, self._LCD_CMD)
        time.sleep(1)


    def output_string(self, message):
#        self.clear_string()
        self._DICT[self._LCD_LINE_1] = message[0:16].center(self._LCD_WIDTH, " ")
        print(message)
        if len(message) > 16:
            self._DICT[self._LCD_LINE_2] = message[16:len(message)].center(self._LCD_WIDTH, " ")

        for i in list(self._DICT.keys()):
            self.lcd_byte(i, self._LCD_CMD)
            for b in range(self._LCD_WIDTH):
                self.lcd_byte(ord(self._DICT[i][b]), self._LCD_CHR)

    # Starts the lcd, enables bits on the screen on some conditions.
    def start(self):
        self.lcd_byte(0x33, self._LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self._LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self._LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self._LCD_CMD)  # 001100 Display On, Cursor Off, Blink Off
        self.lcd_byte(0x28, self._LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self._LCD_CMD)  # 000001 Clear display
        time.sleep(self._E_DELAY)


