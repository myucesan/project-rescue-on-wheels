# !/usr/bin/python
import RPi.GPIO as gpio
import smbus
import socket
import json


class Socket:

    def __init__(self, host="10.3.141.1", port=8808):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
	self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.address = None
        self.message = None
        self.speed = 220
        self.state = None
        self.device = None
        self.data = None
        self.distance = 5
        self.servo = 5;

    def receiveValues(self):

            try:
                self.message, self.address = self.socket.recvfrom(1024)
		#self.data = json.loads(self.message)
  		#self.device = self.data['device']
                #self.state = self.data['state']
                #self.speed = self.data['speed']
                print(self.message)
		
            except socket.error:
                pass

    def sendValues(self):

        if self.address is not None:
                self.socket.sendto(bytes("test", "utf-8"), self.address)
