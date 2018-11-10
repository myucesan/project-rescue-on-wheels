# !/usr/bin/python
import RPi.GPIO as gpio
import smbus
import socket
import json
from couch import *
import time

class Socket:

    def __init__(self, host="10.3.141.1", port=8808):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
	self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
	self.repo = Repository("http://localhost:5984")
        self.repo.selectRepository("rover")
        self.address = None
        self.message = None
        self.speed = 220
        self.state = None
        self.device = None
        self.data = None
        self.distance = 5
        self.servo = 5
	self.lineData = {
        	"state": None,
        	"time": None,
        }
        self.i = 1
        self.counter = 0
	self.docCounter = 0
        self.prevState = None
	self.backtrack = 0

    def receiveValues(self):

            try:
                self.message, self.address = self.socket.recvfrom(1024)
		if self.message is not None:
			self.data = json.loads(self.message.decode())
		if self.data != self.prevJson:
  			self.device = self.data['device']
                	self.state = self.data['state']
                	self.speed = self.data['speed']
                	self.backtrack = self.data['backtrack']
			if self.device == "Webapp":
				if self.counter == 1:
					self.end = time.time()
					self.counter = 0
					self.lineData["state"] = self.prevState
					self.lineData["time"] = self.end - self.begin
                                	self.repo.createDoc(str(self.i), self.lineData)
                                	self.socket.sendto(bytes(json.dumps(self.lineData), "utf-8"), self.address)
                                	self.i = self.i + 1
                            	else:
                                	self.begin = time.time()
                                	self.counter = self.counter + 1

                        self.prevJson = self.data
                        self.prevState = self.state
			self.docCounter += 1

            except socket.error:
                pass

    def sendValues(self):

        if self.address is not None:
                self.socket.sendto(bytes("test", "utf-8"), self.address)
