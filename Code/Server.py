import socket

class Server:

    def __init__(self, host="localhost", port=8762):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False);
        self.socket.bind((host, port))
        self.addresses = []

    def receive(self):

        while True:

            try:
                data = self.socket.recvfrom(1024)

                print(data)

            except socket.error:
                break

server = Server()

while True:
    server.receive()