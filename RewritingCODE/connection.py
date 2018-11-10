# !/usr/bin/python
import socket
import json

class Connection:

    def __init__(self, host="192.168.192.52", port=8025):


            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setblocking(False);
            self.socket.bind((host, port))
            self.address = None

    def receiveData(self):

            try:
                received, self.address = self.socket.recvfrom(4096)
                if received is not None:
                    return json.loads(received.decode())

            except socket.error:
                pass

    def sendData(self, data):

            self.socket.sendto(bytes(json.dumps(data), "utf-8"), self.address)