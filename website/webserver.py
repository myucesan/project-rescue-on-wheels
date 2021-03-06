import sys
sys.path.insert(0, '../')

from gevent import monkey, spawn, sleep
monkey.patch_all()

from flask import Flask, render_template
from flask_socketio import SocketIO
from main import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
main = Main()

@app.route('/')
def main():
    return render_template('templates/index.html')

@app.route('/ControlPage')
def ControlPage():
    return render_template('templates/ControlPage.html')

@socketio.on('direction')
def drive_into_direction(data):
    if not Main().is_disabled():
        Main()._motor_control.drive(data)

@socketio.on('outputString')
def output_string(data):
    if not Main().is_disabled():
        Main()._lcd.output_string(data)

@socketio.on('microphone')
def talk(data):
    print(data)

@socketio.on('LCD')
def change_lcd_output(data):
    print(data)

@socketio.on('backtrack')
def track_back():
    Main().disable()
    Main()._motor_control.reverse_drive()
    Main().enable()

#@socketio.on('light')
#def turn_light(status):
#       print(status)
#def send():
    
 #   while True:
  #      socketio.emit('temperature', "{:.1f}".format(Main()._temperature.convert()))
   #     socketio.emit('compass', Main()._compass.degrees(Main()._compass.heading()))
    #    socketio.emit('distance', "{:.1f}".format((Main()._distance.get_distance())))

def compass():
    while True:
        socketio.emit('compass', Main()._compass.degrees(Main()._compass.heading()))
        

def distance():
    while True:
        socketio.emit('distance', "{:.1f}".format((Main()._distance.get_distance())))        

def temperature():
    while True:
        socketio.emit('temperature', "{:.1f}".format(Main()._temperature.convert()))

def light():
    while True:
        socketio.emit('light', Main()._light.start())
#spawn(send)
spawn(distance)
spawn(compass)
spawn(temperature)
spawn(light)

if __name__ == '__main__':
    print("Starting..")
    socketio.run(app, "10.3.141.1", 8828)
