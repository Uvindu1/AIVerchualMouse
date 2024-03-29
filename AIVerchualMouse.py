import cv2
import numpy as np
import time
import handTrackingModule as htm
import autopy

#################################################
wCam, hCam = 640, 480
frameR = 100 # fream eka adu kirima
#################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detection = htm.handDetector(maxHands=1)
wScr,  hScr = autopy.screen.size()
#print(wScr, hScr)

while True:
    #1.Find hand LandMark
    success, img = cap.read()
    img = detection.findHands(img)
    lmList = detection.findPosition(img)

    #2.Get the tip of the  index and middle fingers
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        print(x1, y1, x2, y2)
    #3.Check which fingers are up
        fingers = detection.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR,frameR), (wCam - frameR, hCam-frameR), (0, 255, 255), 2)
    #4.Only Index Finger: Moving Mode
        if fingers[1]==1 and fingers[2] ==0:
            #5.Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR), (0, hScr))


            #6.Smoothen Values
            #7.Move Mouse
            autopy.mouse.move(x3, y3)#meken thamai mouse eka duwanne
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
    #8.Both Index and middle fingers are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9.Find Distence betweeen fingers
            length, img, lineInfo = detection.findDistense(8, 12, img)
            print(length)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
               #10.Click mouse if distance short
                autopy.mouse.click()

    #11.Frame Rate
    cTime =time.time()
    fps  = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    #12. Display
    cv2.imshow('IMH', img)
    cv2.waitKey(1)















































