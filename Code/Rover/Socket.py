# !/usr/bin/python
import RPi.GPIO as gpio
import smbus
import socket
import json
import time

class Socket:

    def __init__(self, host="10.3.141.1", port=8808):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
	self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.list = []
        self.address = None
        self.message = None
        self.speed = 220
        self.state = None
        self.device = None
        self.data = None
        self.distance = 5
        self.servo = 5
	self.begin = None
	self.end = None
	self.lineData = {
        	"state": None,
        	"time": None,
        }

        self.prevState = None
        self.prevJson = None
	self.backtrack = 0

    def receiveValues(self):

            try:
                self.message, self.address = self.socket.recvfrom(1024)
		if self.message is not None:
			self.data = json.loads(self.message.decode())
        		if self.data != self.prevJson:
				print(self.data)
          			self.device = self.data['device']
                        	self.state = self.data['state']
                        	self.speed = self.data['speed']
                        	self.backtrack = self.data['backtrack']
                        	if self.device == "Webapp":
                                    if self.backtrack == 0:
                                        if self.state != "stop":
                                            self.begin = time.time()
                                        else:
                                            self.end = time.time()
                                            self.lineData["state"] = self.prevState
                                            self.lineData["time"] = self.end - self.begin
                                            self.begin = None
                                            self.list.append({
                                                "state": self.lineData["state"],
                                                "time": self.lineData["time"]
                                            })
                                            self.socket.sendto(bytes(json.dumps(self.lineData).encode("utf-8")), self.address)
            
                                self.prevJson = self.data
                                self.prevState = self.state
			

            except socket.error:
                pass

    def sendValues(self):

        if self.address is not None:
                self.socket.sendto(bytes("test", "utf-8"), self.address)
