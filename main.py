import cv2
import sys
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

import numpy as np
import pandas as pd


# print str(sys.argv[1])

number_of_cycle = int(sys.argv[1])
print " ################## "
print " ##### NUMBER OF CYCLES : " + str(number_of_cycle)
print " ################## "
print " "


#
# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 3. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 4. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 5. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 6. CV_CAP_PROP_FPS Frame rate.
# 7. CV_CAP_PROP_FOURCC 4-character code of codec.
# 8. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 9. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 10. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 11. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 12. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 13. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 14. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 15. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 16. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 17. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 18. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 19. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)



# from espeak import espeak
#
# espeak.set_voice("!v/f5")
#
# espeak.synth("Hi Cristian, Welcome on board, of your BMW !")
#
# while espeak.is_playing:
# 	pass

print (" Importing OBD")
import obd
print ("           ... OK")



# def obd_speed():
#     cmd = obd.commands.SPEED  # select an OBD command (sensor)
#
#     response = connection.query(cmd)  # send the command, and parse the response
#
#     # print(response.value)  # returns unit-bearing values thanks to Pint
#     # print(response.value.to("mph"))  # user-friendly unit conversions
#
#     return response.value


# def obd_speed():
#     connection = obd.OBD()  # auto-connects to USB or RF port
#     cmd = obd.commands.SPEED  # select an OBD command (sensor)
#
#     response = connection.query(cmd)  # send the command, and parse the response
#
#     # print(response.value)  # returns unit-bearing values thanks to Pint
#     # print(response.value.to("mph"))  # user-friendly unit conversions
#
#     return response.value
# Remember !!!!!
# sudo apt-get install autoconf gettext libtool libjpeg62-dev
# cd v4l-utils
# autoreconf -vfi
# ./configure
# make
# sudo make install
# otherwise the cv2 videocapture will not work with picamera !!!
# sudo apt-get install v4l-utils



# # Initiate video capture for video file
print (" Initializing video capture")
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)
#

i = 0

output_data = [['filename',\
                'throttle_position', \
                'steering_angle',\
                'speed',\
                'fuel level',\
                'CONTROL_MODULE_VOLTAGE',\
                'AMBIANT_AIR_TEMP',\
                'oil_temperature',\
                'accelerator',\
                'time_frame',\
                'time_OBD']]

connection = obd.OBD()  # auto-connects to USB or RF port
cmd_speed = obd.commands.SPEED  # select an OBD command (sensor)
cmd_FUEL_LEVEL = obd.commands.FUEL_LEVEL
CONTROL_MODULE_VOLTAGE = obd.commands.CONTROL_MODULE_VOLTAGE
AMBIANT_AIR_TEMP = obd.commands.AMBIANT_AIR_TEMP
OIL_TEMP = obd.commands.OIL_TEMP
RELATIVE_ACCEL_POS =  obd.commands.RELATIVE_ACCEL_POS

print " ######"
print " ######"
print " Starting while ..."
print " ######"
print " ######"
# while cap.isOpened() and i < 100:

while i < number_of_cycle:

    i = i + 1
    time.sleep(.1)
    # Read first frame
    time_before = time.time()
    # grab an image from the camera
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array

    time_frame = time.time() - time_before
    # print " time to grab a new image " + str(time_frame)

    filename = 'img/photo_' + str(i)  + '.jpg'
    throttle_position = 0
    steering_angle = 1
    time_before = time.time()
    response = connection.query(cmd_FUEL_LEVEL, force=True)
    fuel_level = response.value
    response = connection.query(cmd_speed, force=True)
    speed = response.value
    response = connection.query(CONTROL_MODULE_VOLTAGE, force=True)
    voltage = response.value
    response = connection.query(AMBIANT_AIR_TEMP, force=True)
    ambient_temp = response.value
    response = connection.query(OIL_TEMP, force=True)
    oil_temperature = response.value

    response = connection.query(RELATIVE_ACCEL_POS, force=True)
    accelerator = response.value


    time_OBD = time.time() - time_before

    # print (" speed = " + str(speed) +  " fuel level = " + str(fuel_level)+" file= " + filename) + " time frame " + str(time_frame ) + " time speed" + str(time_OBD)
    time_before= time.time()
    cv2.imwrite(filename, image)
    # print "time for writing " + str ( time.time() - time_before)


    output_data.append([filename,throttle_position, steering_angle, str(speed), \
                        str(fuel_level),str(voltage),str(ambient_temp), \
                        str(oil_temperature),str(accelerator), \
                        str(time_frame), str(time_OBD)])

connection.close()


# cap.release()
# # out.release()
# # cv2.destroyAllWindows()
df = pd.DataFrame(np.array(output_data))
df.to_csv("car_output_data.csv")
