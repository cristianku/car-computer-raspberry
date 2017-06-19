print " Importing PiRGBArray ...."
from picamera.array import PiRGBArray
print " Importing PiCamera ...."
from picamera import PiCamera
import time
import threading
import cv2

from Queue import deque


class camera():
    def __init__(self):
        self.red_light = False
        self.i = 0
        self.camera = PiCamera()
        self.camera.framerate = 30
        self.camera.resolution = (2592, 1952)
        # camera.resolution = (800,600)
        self.camera.iso = 100  # auto

        # camera.start_preview()

        self.rawCapture = PiRGBArray(camera)
        self.images_queue = deque()

        # allow the camera to warmup
        time.sleep(0.1)

    def capture(self):
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, use_video_port=True, format="bgr")
        self.image = self.rawCapture.array


    def write_image_to_file(self):
        self.red_light == True
        print " -- write_image_to_file "
        while self.images_queue:
            print " -------- while  -------"
            img = self.images_queue.popleft()
            self.i += 1
            filename = 'img/photo_' + str(self.i) + '.jpg'
            print "writing " + filename
            cv2.imwrite(filename, img)
        self.red_light == False


    def write_image(self):
        self.images_queue.append(self.image)
        if len(self.images_queue) > 10 and self.red_light == False:
            print " ******** "
            print len(self.images_queue)
            self.write_image_to_file()
            writing = threading.Thread(target=self.write_image_to_file)
            print " ******** "

    # t_left_led = threading.Thread(target=left_led.turn_on)
