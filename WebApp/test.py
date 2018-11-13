from flask import Flask, render_template
from flask_socketio import SocketIO
from MotorInitialization import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
variabele = 0
@socketio.on('direction')
def drive_into_direction(data):
	MotorInitialization().drive(data)
	
	
@socketio.on('microphone')
def talk(data):
	print(data)

@socketio.on('LCD')
def change_lcd_output(data):
	print(data)

@socketio.on('light')
def turn_light(status):
	print(status)

@socketio.on('backtrack')
def track_back(status):
	print(status)

if __name__ == '__main__':
    socketio.run(app, "10.3.141.1", 8816)
