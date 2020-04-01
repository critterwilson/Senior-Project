#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 08:58:31 2020

@author: CritterWilson
"""
import pafy
import cv2
import imutils
import time
import numpy as np
import sys
import logging
from imutils.video import VideoStream
from imutils.video import FPS

# get the URL from the command line argument
url = sys.argv[1]

# All of the possible classes in our model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
# We don't give a rat's patootie about anything but "Person"
IGNORE = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
# assign random colors to each class
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# create new stream from url
vPafy = pafy.new(url)
# get the best quality video (no audio)
play = vPafy.getbestvideo(preftype="webm")
# our threshold (classify as a class if we are over 1% sure)
## Note that since we are only looking for people, we shouldn't have an issue
## with such a low threshold value.
threshold = 0.01
# the model we are going to be using
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", 
                               "MobileNetSSD_deploy.caffemodel")
#start the video
stream = cv2.VideoCapture(play.url)
while (True):
    ret,frame = stream.read()
    frame = imutils.resize(frame, width=300)

     # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    # create a blob (a 4d image that is easier to compare)
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
 		0.007843, (300, 300), 127.5)

 	# pass the blob through the network and obtain the detections and
 	# predictions
    net.setInput(blob)
    detections = net.forward()

 	# loop over the detections
    for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
        confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
        if confidence > threshold:
 			# extract the index of the class label from the
 			# `detections`, then compute the (x, y)-coordinates of
 			# the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] in IGNORE:
                continue
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

 			# draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    # User controls
    key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break 
    # if the 'p' key was pressed, pause for an hour, push any key to continue
    if key == ord("p"):
        cv2.waitKey(3600000)

stream.release()
cv2.destroyAllWindows()