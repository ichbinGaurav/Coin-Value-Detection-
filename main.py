# pip install opencv-python
# pip install cvzone

import cv2
import cvzone
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3,640) # width
cap.set(4,480) # height

totalMoney = 0

# 2.2

def empty(a):
    pass

# 2.1

cv2.namedWindow("Settings")
cv2.resizeWindow("Settings",640,240)
cv2.createTrackbar("Threshold1","Settings",50,255,empty)
cv2.createTrackbar("Threshold2","Settings",10,255,empty)

# 2
def preProcessing(img):
    imgPre = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgPre = cv2.GaussianBlur(imgPre,(5,5),3)

    threshold1 = cv2.getTrackbarPos("Threshold1","Settings")
    threshold2 = cv2.getTrackbarPos("Threshold2","Settings")
    imgPre = cv2.Canny(imgPre,102,233)
    
    # imgPre = cv2.Canny(imgPre,threshold1,threshold2)

    kernel = np.ones((3,3),np.uint8)
    imgPre = cv2.dilate(imgPre, kernel,iterations=1)
    imgPre = cv2.morphologyEx(imgPre,cv2.MORPH_CLOSE, kernel)
   
    return imgPre

# 1
while True:
    sucess,img = cap.read()
    imgPre = preProcessing(img)

    imgContours,conFound = cvzone.findContours(img,imgPre,minArea=20)

    totalMoney = 0
    num = 0
    if conFound:
        for contour in conFound:
            peri = cv2.arcLength(contour['cnt'],True)
            approx= cv2.approxPolyDP(contour['cnt'],0.02*peri,True)

            # x = 300
            if len(approx) > 5:
                num = num+1
                area = contour['area'] 
                print(area)
                if 2500<area<2800:
                    totalMoney += 2
                elif 2200<area<2500:
                    totalMoney += 1
                elif 1950<area<2180:
                    totalMoney += 0.20
                elif 1625<area<1750:
                    totalMoney += 0.10
                elif 1300<area<1600:
                    totalMoney += 0.02
                else:
                    totalMoney += 0.01

    # print("Total = " + str(totalMoney))

    imgCombined = cvzone.stackImages([imgPre,imgContours],2,1)
    # cv2.imshow("Image",img)
    # cv2.imshow("ImagePre",imgPre)
    
    formatted_number = "{:.2f}".format(totalMoney)

    font = cv2.FONT_HERSHEY_PLAIN
    scale = 2
    thickness = 2

    cv2.putText(imgCombined, f"{formatted_number} Euro", (200, 40), font, scale, (0, 255, 0), thickness)
    cv2.putText(imgCombined, f"Coins = {num}", (200, 75), font, scale, (0,0,255), thickness)


    cv2.imshow("Output",imgCombined)
    cv2.waitKey(1)

    