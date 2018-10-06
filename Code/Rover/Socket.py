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
        self.socket.setblocking(False);
        self.socket.bind((host, port))
        self.addresses = []

    def getState(self):

        while True:

            try:
                data, address = self.socket.recvfrom(1024)
                return data.decode("utf-8")
            except socket.error:
                break
