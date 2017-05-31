import cv2

import time
# Initiate video capture for video file
cap = cv2.VideoCapture('./videos/video2.m4v')
from  car_recognition import car_recognition

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter()
succes = out.open('./videos/output.mp4v',fourcc, 30.0, (1280,720),True)


import graph_utils
from lane_detection import lane_detection

i = 0
while True== True:
    i = i  +1
    ret, frame = cap.read()
    # Read first frame


    frame1 =   lane_detection(frame).detection()

    frame2 = car_recognition(frame1, frame1).recognize()

    cv2.imshow(' ', frame2)
    # out.write(frame2)

    if cv2.waitKey(1) == 13: #13 is the Enter Key
             break

cap.release()
out.release()
cv2.destroyAllWindows()
