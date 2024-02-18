import cv2
import tensorflow
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
from cvzone.ClassificationModule import Classifier
import pyttsx3
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("model/keras_model.h5", "model/labels.txt")

offset = 20
imgSize = 300

labels = ['All', 'Ball', 'Cat']

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal)/2)
            imgWhite[:, wGap:wCal+wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal+hGap, :] = imgResize

            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)

        cv2.rectangle(imgOutput, (x-offset, y-offset-50), (x-offset+90, y-offset+26), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y-20), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)
        text_to_speech(labels[index])
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
