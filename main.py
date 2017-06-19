# http://obdcon.sourceforge.net/2010/06/obd-ii-pids/


#
# print " ################## "
# print " Connecting to RFCOMM "
# from subprocess import Popen, PIPE
#
# cmd = 'sudo rfcomm connect 0  00:1D:A5:68:98:8A &'
# p = Popen(cmd , shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
# output, err = p.communicate()
# rc = p.returncode
#
# print " ... connected - return code = " + str(rc) + " " + str( err) + str(output)
#
# exit()
#
print " Importing cv2 ...."
import cv2
print " Importing sys ...."
import sys
print " Importing time ...."
import time
print " Importing PiRGBArray ...."
from picamera.array import PiRGBArray
print " Importing PiCamera ...."
from picamera import PiCamera

print " Importing numpy ...."
import numpy as np
print " Importing  obd2Reader ...."
import obd2Reader
print " .. ok "
# print str(sys.argv[1])

number_of_cycle = int(sys.argv[1])
print " ################## "
print " ##### NUMBER OF CYCLES : " + str(number_of_cycle)
print " ################## "
print " "

# from espeak import espeak
#
# espeak.set_voice("!v/f5")
#
# espeak.synth("Hi Cristian, Welcome on board, of your BMW !")
#
# while espeak.is_playing:
# 	pass



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


print (" Creating obd2Reader .....")
obdConn = obd2Reader.obd2Reader()
print ("           ... OK")


# # Initiate video capture for video file
print (" Initializing video capture")
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)
#

i = 0

output_data = [['filename',                 \
                'throttle_position',        \
                'steering_angle',           \
                'speed',                    \
                'fuel level',               \
                'CONTROL_MODULE_VOLTAGE',   \
                'AMBIANT_AIR_TEMP',         \
                'oil_temperature',          \
                'accelerator_b',            \
                'accelerator_d',            \
                'throttle  ',               \
                'engine run time',          \
                'time_frame',               \
                'time_OBD']]


print " ######"
print " ######"
print " Starting while ..."
print " ######"
print " ######"
# while cap.isOpened() and i < 100:
while i < number_of_cycle and obdConn.connected :
    i = i + 1
    # time.sleep(.1)
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
    speed               = obdConn.speed
    print speed
    if speed == None or str(speed) == "None": break

    fuel_level          = obdConn.fuel_level
    voltage             = obdConn.voltage
    ambient_temp        = obdConn.ambiant_air_temp
    oil_temperature     = obdConn.oil_temp
    accelerator_b       = obdConn.throttle_b   # response = connection.query(RELATIVE_ACCEL_POS, force=True)
    accelerator_d       = obdConn.accelerator_d  # response = connection.query(RELATIVE_ACCEL_POS, force=True)
    throttle            = obdConn.throttle_act
    run_time            = obdConn.run_time


    # accelerator = response.value
    accelerator = 0

    time_OBD = time.time() - time_before

    # print (" speed = " + str(speed) +  " fuel level = " + str(fuel_level)+" file= " + filename) + " time frame " + str(time_frame ) + " time speed" + str(time_OBD)
    time_before= time.time()
    cv2.imwrite(filename, image)
    # print "time for writing " + str ( time.time() - time_before)


    output_data.append([filename,throttle_position, steering_angle, str(speed), \
                        str(fuel_level),str(voltage),str(ambient_temp), \
                        str(oil_temperature),   \
                        str(accelerator_b),     \
                        str(accelerator_d),     \
                        str(throttle),          \
                        str(run_time),          \
                        str(time_frame), str(time_OBD)])

    if i % 10 == 0: print " reading number = " + str(i) + " engine run time " + str(run_time)

obdConn.close()


# cap.release()
# # out.release()
# # cv2.destroyAllWindows()
import pandas as pd

df = pd.DataFrame(np.array(output_data))
df.to_csv("car_output_data.csv")
