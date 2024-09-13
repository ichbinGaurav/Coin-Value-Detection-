# pip install opencv-python

import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3,640) # width
cap.set(4,480) # height

totalMoney = 0

# 2.2

def empty(a):
    pass

# 2.1

cv2.namedWindow("Threshold Bar")
cv2.resizeWindow("Threshold Bar",640,240)
cv2.createTrackbar("Threshold1","Threshold Bar",50,255,empty)
cv2.createTrackbar("Threshold2","Threshold Bar",10,255,empty)

# 2
def preProcessing(img):
    imgPre = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgPre = cv2.GaussianBlur(imgPre,(5,5),3)

    threshold1 = cv2.getTrackbarPos("Threshold1","Threshold Bar")
    threshold2 = cv2.getTrackbarPos("Threshold2","Threshold Bar")
    # imgPre = cv2.Canny(imgPre,102,233)
    imgPre = cv2.Canny(imgPre,99,55)
    
    # imgPre = cv2.Canny(imgPre,threshold1,threshold2)

    kernel = np.ones((3,3),np.uint8)
    imgPre = cv2.dilate(imgPre, kernel,iterations=1)
    imgPre = cv2.morphologyEx(imgPre,cv2.MORPH_CLOSE, kernel)
   
    return imgPre

# 1
while True:
    sucess,img = cap.read()
    imgPre = preProcessing(img)

    conFound = []
    imgContours = img.copy()
    contours, hierarchy = cv2.findContours(imgPre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # retrieves only the external contours
    # stores all the contour points without approximating

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 20 < area :
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # cv2.arcLength calculates the perimeter of the contour.
            # cnt is the current contour being processed.
            # True indicates that the contour is a closed curve (it forms a closed loop).
            # approx = cv2.approxPolyDP(cnt, 0.02 * peri, True):

            # cv2.approxPolyDP approximates a polygonal curve to the contour with a specified epsilon.
            # cnt is the input contour.
            # 0.02 * peri is the epsilon parameter, determining the approximation accuracy. Smaller epsilon values result in a closer approximation to the original contour.
            # True indicates that the approximated polygon is a closed curve.

            cv2.drawContours(imgContours, cnt, -1, (0,0,255), 2)
            x, y, w, h = cv2.boundingRect(approx)

            cx, cy = x + (w // 2), y + (h // 2)
            conFound.append({"cnt": cnt, "area": area, "bbox": [x, y, w, h], "center": [cx, cy]})

    conFound = sorted(conFound, key=lambda x: x["area"], reverse=True)

    totalMoney = 0
    num = 0
    if conFound:
        for contour in conFound:
            peri = cv2.arcLength(contour['cnt'],True)
            approx= cv2.approxPolyDP(contour['cnt'],0.02*peri,True)

            if len(approx) > 5:
                num = num+1
                area = contour['area'] 
                print(area)
                if 3200<area<3500:
                    totalMoney += 2
                elif 2750<area<2950:
                    totalMoney += 1
                elif 26000<area<2700:
                    totalMoney += 0.20
                elif 1950<area<2150:
                    totalMoney += 0.10
                elif 1700<area<1900:
                    totalMoney += 0.02
                else:
                    totalMoney += 0.01

    # print("Total = " + str(totalMoney))

    cv2.imshow("Image",imgPre)
    # cv2.imshow("ImagePre",imgContours)
    
    formatted_number = "{:.2f}".format(totalMoney)

    
    text = f"{formatted_number} Euro"
    font = cv2.FONT_HERSHEY_PLAIN
    scale = 2
    thickness = 2

    colorT=(0, 255, 0)

    cv2.putText(imgContours, text, (50, 40), font, scale, colorT, thickness)
    cv2.putText(imgContours, f"Coins = {num}", (50, 75), font, scale, colorT, thickness)

    cv2.imshow("Output",imgContours)
    cv2.waitKey(1)

