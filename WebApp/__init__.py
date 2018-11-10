from gevent import monkey, spawn, sleep
monkey.patch_all()

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
import socket
import json
from threading import *

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
list = []
thread = None
@app.route('/')
def main():
	return render_template('index.html')

@app.route('/ControlPage')
def ControlPage():
	return render_template('ControlPage.html')
	
@socketio.on('roverConnection')
def startConnection(roverInfo):
	test = json.loads(roverInfo)
	server_ip = test['ip']
	port = test['port']
	server_addres = (server_ip, port)
	list.append(server_addres)	

@socketio.on('roverControl')
def controlRover(data):
	
	print("controlRovermethod")
	print("data")
	socket.sendto(bytes(data, "utf-8"), list[0])	

def test():
	prevMes = None
	while True:
		
		
		if list:
			message, address = socket.recvfrom(1024)
			print(message)
			if prevMes == None or prevMes != message:
				socketio.emit('lineDrawer', message.decode())
		sleep(0.1)
spawn(test)

if __name__ == '__main__':
    socketio.run(app, "192.168.137.8", 9928)
