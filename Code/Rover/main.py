from Socket import *
from MotorInitialization import *

MotorInitialization = MotorInitialization()

def MotorControl():
    socket = Socket()
    while True:
        socket.receiveValues()

        if socket.state == "forward":
            MotorInitialization.forward()
        if socket.state == "right":
            MotorInitialization.right()
        if socket.state == "left":
            MotorInitialization.left()
        if socket.state == "backward":
            MotorInitialization.backward()
        if socket.state == "stop":
            MotorInitialization.stop()

        MotorInitialization.setSpeed(socket.speed)

def main():
    print("main invoked")
    thread = Thread(target=MotorControl)
    thread.start()
    thread.join()

main()
