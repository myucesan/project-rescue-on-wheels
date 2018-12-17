#!/usr/bin/python
'''
	Author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import constant
import os
from db import *
import cv2
from PIL import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time

# Initialize how many samples of individual's face must be taken until stop
ENDCOUNT = 30

# Declare and initialize video capture object to None
capture = None

path = "User/"

print("\n [INFO] Initializing face capture. Look the camera and wait ...")


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            face_detector = cv2.CascadeClassifier('/home/pi/row/frdynamicweb/fr/Cascades/haarcascade_frontalface_default.xml')

            # Declare and initialize individual sampling face count
            count = 0
            id = DB().add_face(path)
            os.makedirs("{}{}".format(path, id))
            while True:
                try:
                    rc, img = capture.read()
                    if not rc:
                        continue
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        count += 1

                        # Save the captured image into the datasets folder
                        cv2.imwrite("{}{}/{}.jpg".format(path, id, count), gray[y:y + h, x:x + w])

                    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    jpg = Image.fromarray(imgRGB)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile, 'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                    time.sleep(0.05)

                    # Stop gathering data when requested amount of images of individual face have been taken.
                    if count >= ENDCOUNT:
                        break
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://"{}":{}/cam.mjpg"/>'.format(constant.IP, constant.PORT))
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global capture
    capture = cv2.VideoCapture(0)

    global img
    try:
        server = ThreadedHTTPServer((constant.IP, constant.PORT), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n [INFO] Exiting Program and cleanup stuff")
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()
