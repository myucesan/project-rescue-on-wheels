from Socket import *
from MotorInitialization import *

MotorInitialization = MotorInitialization()

def MotorControl():
    socket = Socket()
    while True:
        state = socket.getState()
        if state == "forward":
            MotorInitialization.forward()
        if state == "right":
            MotorInitialization.right()
        if state == "left":
            MotorInitialization.left()
        if state == "backward":
            MotorInitialization.backward()
        if state == "stop":
            MotorInitialization.stop()

def main():
    thread = Thread(target=MotorControl)
    MotorInitialization.motorSetUp()
    thread.start()
    thread.join()

main()