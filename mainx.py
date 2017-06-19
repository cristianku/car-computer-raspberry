import cv2

import time
# import picamera
import numpy as np
import pandas as pd

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

# # Initiate video capture for video file
print (" Initializing video capture")
cap = cv2.VideoCapture(0)
print ("           ... OK")
cap.set(3,800)
cap.set(4,600)

time.sleep(2)
ret, frame = cap.read()

i = 0

output_data = [['filename','throttle_position', 'steering_angle','speed','time_frame','time_speed']]


print " ######"
print " ######"
print " Starting while ..."
print " ######"
print " ######"
while cap.isOpened() and i < 20:
    i = i + 1
    time.sleep(.05)
    # Read first frame
    time_before = time.time()
    ret, frame = cap.read()
    time_frame = time.time() - time_before

    filename = 'img/photo_' + str(i)  + '.jpg'
    throttle_position = 0
    steering_angle = 1
    time_before = time.time()
    connection = obd.OBD()  # auto-connects to USB or RF port
    cmd_speed = obd.commands.SPEED  # select an OBD command (sensor)
    response = connection.query(cmd_speed)
    speed = response.value
    # speed = 0
    time_speed = time.time() - time_before

    print (" speed = " + str(speed) + " file= " + filename) + " time frame " + str(time_frame ) + " time speed" + str(time_speed)
    time_before = time.time()
    cv2.imwrite(filename, frame)
    print "time for writing " + str ( time.time() - time_before)


    output_data.append([filename,throttle_position, steering_angle, str(speed), str(time_frame), str(time_speed)])


cap.release()
# out.release()
cv2.destroyAllWindows()
df = pd.DataFrame(np.array(output_data))
df.to_csv("car_output_data.csv")
