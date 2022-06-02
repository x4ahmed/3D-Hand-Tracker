import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Webcam
width = 720
height = 1280
cap = cv2.VideoCapture(0)
cap.set(3,height)
cap.set(4,width)
success, img = cap.read()
h, w, _ = img.shape

# Hand Detector
detector = HandDetector(maxHands=2, detectionCon=0.8)

# Communication
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 8000)

while True:
    # Get the frame
    success, img = cap.read()

    # Detect hands
    hands, img = detector.findHands(img)

    # Get landmarks
    data = []
    if hands:
        # Get the first hand
        hand = hands[0]
        lmList = hand['lmList']

        # Reversing y coordinates
        for lm in lmList:
            data.extend([lm[0],h - lm[1],lm[2]])
        #print(data)

        # Send the data using udp connection
        socket.sendto(str.encode(str(data)), serverAddressPort)

    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow("Hand Tracker", img)
    cv2.waitKey(1)