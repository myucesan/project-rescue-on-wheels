from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
import socket
import json

app = Flask(__name__)
socketio = SocketIO(app)
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
list = []
@app.route('/')
def main():
	return render_template('index.html')

@app.route('/ControlPage')
def ControlPage():
	return render_template('ControlPage.html')

@socketio.on('message')
def handle_message(message):
	socket.sendto(bytes("UDP en Websockets werken tegelijkertijd", "utf-8"), server_addres)
	
@socketio.on('roverConnection')
def startConnection(roverInfo):
	test = json.loads(roverInfo)
	server_ip = test['ip']
	port = test['port']
	server_addres = (server_ip, port)
	list.append(server_addres)
	socket.sendto(bytes("test", "utf-8"), server_addres)	

@socketio.on('roverControl')
def controlRover(key):
	socket.sendto(bytes(key, "utf-8"), list[0])	

if __name__ == '__main__':
    socketio.run(app, "192.168.137.102", port=8499)

