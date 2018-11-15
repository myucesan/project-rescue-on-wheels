# !/usr/bin/python

import RPIO.GPIO as GPIO
import time


class LCD:

    _LCD_RS = None
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

        GPIO.setboard(GPIO.BOARD)
        GPIO.setup(self._LCD_E, GPIO.OUT)
        GPIO.setup(self._LCD_RS, GPIO.OUT)
        GPIO.setup(self._LCD_D4, GPIO.OUT)
        GPIO.setup(self._LCD_D5, GPIO.OUT)
        GPIO.setup(self._LCD_D6, GPIO.OUT)
        GPIO.setup(self._LCD_D7, GPIO.OUT)

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

    def output_string(self, message, line, style):

        if style == 1:
            message = message.ljust(self._LCD_WIDTH, " ")
        elif style == 2:
            message = message.center(self._LCD_WIDTH, " ")
        elif style == 3:
            message = message.rjust(self._LCD_WIDTH, " ")

        self.lcd_byte(line, self._LCD_CMD)

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[1]), self._LCD_CHR)

    def start(self):

        self.lcd_byte(0x33, self._LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self._LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self._LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self._LCD_CMD)  # 001100 Display On, Cursor Off, Blink Off
        self.lcd_byte(0x28, self._LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self._LCD_CMD)  # 000001 Clear display
        time.sleep(self._E_DELAY)


lcd = LCD()
lcd.start()
lcd.output_string("Testing", lcd._LCD_LINE_1, 2)
