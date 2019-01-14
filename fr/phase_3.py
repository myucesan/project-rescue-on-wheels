#!/usr/bin/python
'''
	Author: Yoshio Schermer
	MJPG streamer with OpenCV
'''
import constants
import os
import cv2
from PIL import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# Initiate id counter
id = 0

# Names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Bean']

# Declare and initialize video capture object to None
capture = None


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()

            # Define min window size to be recognized as a face
            minW = 0.1 * capture.get(3)
            minH = 0.1 * capture.get(4)

            while True:
                try:
                    rc, img = capture.read()
                    if not rc:
                        continue
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(int(minW), int(minH)),
                    )

                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                        # Check if confidence is less them 100 ==> "0" is perfect match
                        if (confidence < 100):
                            id = names[id]
                            confidence = "  {0}%".format(round(100 - confidence))
                        else:
                            id = "unknown"
                            confidence = "  {0}%".format(round(100 - confidence))

                        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

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
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://"{}":{}/cam.mjpg"/>'.format(constants.IP, constants.PORT))
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global capture
    capture = cv2.VideoCapture(0)

    global img
    try:
        print(constants.IP + " ")
        print(constants.PORT)
        server = ThreadedHTTPServer((constants.IP, constants.PORT), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n [INFO] Exiting Program and cleanup stuff")
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()

