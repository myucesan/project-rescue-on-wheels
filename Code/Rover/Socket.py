# !/usr/bin/python
import RPi.GPIO as gpio
import smbus
import time
from threading import *
from curtsies import Input
import socket


class Socket:

    def __init__(self, host="10.3.141.1", port=8712):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.socket.bind((host, port))
        self.address = None
        self.message = None
        self.speed = None
        self.state = None
        self.data = None

    def receiveValues(self):

        while True:

            try:
                self.message, self.address = self.socket.recvfrom(1024)
                self.data = json.loads(self.message)
                self.state = self.data['state']
                self.speed = self.data['speed']


            except socket.error:
                break
