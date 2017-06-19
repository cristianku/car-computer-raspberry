# import the necessary packages
from picamera.array import PiRGBArray
import picamera
import picamera.array
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = picamera.PiCamera()
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')

vidwrite = cv2.VideoWriter('/home/pi/python/videos/camera.mp4v',fourcc, 15.0, (1280,720),True)


# allow the camera to warmup


camera.start_preview()
i = 0
while i < 25:
    i += 1
    # grab an image from the camera
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        image = stream.array

    frame2 = cv2.resize(image, None, fx=0.5, fy=0.5,  interpolation=cv2.INTER_LINEAR)  # display the image on screen and wait for a keypress
    cv2.imwrite("/home/pi/python/imgs/camera_still.jpg", frame2)
    print " write frame2 "
    vidwrite.write(frame2)

vidwrite.release()
