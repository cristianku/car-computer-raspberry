print " Importing PiRGBArray ...."
from picamera.array import PiRGBArray
print " Importing PiCamera ...."
from picamera import PiCamera
import time
import threading
import cv2

from Queue import deque


class camera():
    def __init__(self, filedir):
        print " ********** "
        print " Initializing camera"
        print " ********** "
        print " ********** "
        print " ********** "
        print " ********** "
        print " ********** "
        self.red_light = False
        self.i = 0
        self.camera_conn = PiCamera()
        self.camera_conn.framerate = 30
        # self.camera_conn.resolution = (2592, 1952)
        self.camera_conn.brightness = 50

        self.camera_conn.resolution = (1920,1088)
        self.camera_conn.iso = 100  # auto

        self.camera_conn.start_preview()

        self.rawCapture = PiRGBArray(self.camera_conn)
        self.images_queue = deque()
        self.filedir = filedir

        # allow the camera to warmup
        time.sleep(0.1)

    def capture(self):
        self.rawCapture.truncate(0)
        self.camera_conn.capture(self.rawCapture, use_video_port=False, format="bgr")
        self.image = self.rawCapture.array

    def write_image_to_file(self):
        self.red_light == True
        while self.images_queue:
            img = self.images_queue.popleft()
            self.i += 1
            filename = self.filedir + 'photo_' + str(self.i) + '.jpg'
            if self.i % 5 == 0:
                print "writing " + filename
            cv2.imwrite(filename, img)
        self.red_light == False


    def write_image(self):
        self.images_queue.append(self.image)
        if len(self.images_queue) > 20 and self.red_light == False:
            # print " ******** "
            # print len(self.images_queue)
            # self.write_image_to_file()
            writing = threading.Thread(target=self.write_image_to_file)
            writing.start()
            # print " ******** "
    def close(self):
        camera.stop_preview()

        # t_left_led = threading.Thread(target=left_led.turn_on)
