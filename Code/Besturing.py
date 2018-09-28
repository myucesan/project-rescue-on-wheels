import socket
from MotorControl import *
from threading import *

class Besturing:

    def __init__(self, host="145.28.165.201", port=8762):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False);
        self.socket.bind((host, port))
        self.addresses = []
        self.motor = MotorControl()

    def control(self):

        while True:

            try:
                data, address = self.socket.recvfrom(1024)

                if data.decode("utf-8") == "forward":
                    self.motor.forward()
                if data.decode("utf-8") == "right":
                    self.motor.right()
                if data.decode("utf-8") == "left":
                    self.motor.left()
                if data.decode("utf-8") == "backward":
                    self.motor.backward()
                if data.decode("utf-8") == "stop":
                    self.motor.stop()

            except socket.error:
                break

def main():
    besturing = Besturing()
    thread = Thread(target = besturing.control())
    while True:
        thread.start()
        thread.join()

