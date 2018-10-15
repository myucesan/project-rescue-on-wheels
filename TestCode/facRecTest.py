import cv2
import sys

#Get user supplies values
imagePath = sys.argv[1]
cascPath = sys.argv[2]

#Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

#Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converts image to greyscale, processing mostly done in greyscale

# Detect faces in the image
face = faceCascade.detectMultiScale(
	gray,
	scaleFactor=1.1,
	minNeighbors=5,
	minSize=(30, 30),
	flags = cv2.cv.CV_HAAR_SCALE_IMAGE
)

print "Found {0} faces!".format(len(faces))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
	cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display image and wait for user input before proceeding
cv2.imshow("Faces found", image)
cv2.waitKey(0)
