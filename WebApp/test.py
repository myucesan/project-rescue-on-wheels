import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket.sendto(bytes("test", "utf-8"), ("192.168.192.52", 8802))
