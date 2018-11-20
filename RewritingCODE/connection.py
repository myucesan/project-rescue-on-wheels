# !/usr/bin/python
import socket
import json

class Connection:

    _socket = None
    _address = None
    _received = None
    
    def __init__(self, host="192.168.192.52", port=8025):


            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setblocking(False);
            self._socket.bind((host, port))
            self._address = None

    def receive_data(self):

            try:
                self._received, self._address = self.socket.recvfrom(4096)
                if received is not None:
                    return json.loads(received.decode())

            except socket.error:
                pass

    def send_data(self, data):

            self.socket.sendto(bytes(json.dumps(data), "utf-8"), self.address)
