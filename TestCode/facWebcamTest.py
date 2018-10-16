#written by Team2; Metabots

import sys
import cv2

cascPath = sys.argv[1]
faceCascade = cv2.cascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while true:
	# Capture frame-by-frame
	ret, frame = video_capture.read()
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# The actual face detecting
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	#Drawing the rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	#display the resulting frame
	cv2.imshow('Video', frame)

	# Press 'q' to stop the script running
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#when everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
