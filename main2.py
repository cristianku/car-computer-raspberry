import obd

import cv2

import time
import picamera
import numpy as np
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

################ da spostare in classe esterna ############
#
# import talkey
# tts = talkey.Talkey(
#     # These languages are given better scoring by the language detector
#     # to minimise the chance of it detecting a short string completely incorrectly.
#     # Order is not important here
#     preferred_languages=['en', 'af', 'el', 'fr'],
#
#     # The factor by which preferred_languages gets their score increased, defaults to 80.0
#     preferred_factor=80.0,
#
#     # The order of preference of using a TTS engine for a given language.
#     # Note, that networked engines (Google, Mary) is disabled by default, and so is dummy
#     # default: ['google', 'mary', 'espeak', 'festival', 'pico', 'flite', 'dummy']
#     # This sets eSpeak as the preferred engine, the other engines may still be used
#     #  if eSpeak doesn't support a requested language.
#     engine_preference=['espeak'],
#
#     # Here you segment the configuration by engine
#     # Key is the engine SLUG, in this case ``espeak``
#     espeak={
#         # Specify the engine options:
#         'options': {
#             'enabled': True,
#         },
#
#         # Specify some default voice options
#         'defaults': {
#                 'words_per_minute': 150,
#                 'variant': 'f4',
#         },
#
#         # Here you specify language-specific voice options
#         # e.g. for english we prefer the mbrola en1 voice
#         'languages': {
#             'en': {
#                 'voice': 'english-mb-en1',
#                 'words_per_minute': 130
#             },
#         }
#     }
# )
#
# tts.say('Hi Cristian ! Welcome on board of your bmw !')

# Pty Language Age/Gender VoiceName          File          Other Languages
#  5  af             M  afrikaans            other/af
#  5  an             M  aragonese            europe/an
#  5  bg             -  bulgarian            europe/bg
#  5  bs             M  bosnian              europe/bs
#  5  ca             M  catalan              europe/ca
#  5  cs             M  czech                europe/cs
#  5  cy             M  welsh                europe/cy
#  5  da             M  danish               europe/da
#  5  de             M  german               de
#  5  el             M  greek                europe/el
#  5  en             M  default              default
#  2  en-gb          M  english              en            (en-uk 2)(en 2)
#  5  en-sc          M  en-scottish          other/en-sc   (en 4)
#  5  en-uk-north    M  english-north        other/en-n    (en-uk 3)(en 5)
#  5  en-uk-rp       M  english_rp           other/en-rp   (en-uk 4)(en 5)
#  5  en-uk-wmids    M  english_wmids        other/en-wm   (en-uk 9)(en 9)
#  2  en-us          M  english-us           en-us         (en-r 5)(en 3)
#  5  en-wi          M  en-westindies        other/en-wi   (en-uk 4)(en 10)
#  5  eo             M  esperanto            other/eo
#  5  es             M  spanish              europe/es
#  5  es-la          M  spanish-latin-am     es-la         (es-mx 6)(es 6)
#  5  et             -  estonian             europe/et
#  5  fa             -  persian              asia/fa
#  5  fa-pin         -  persian-pinglish     asia/fa-pin
#  5  fi             M  finnish              europe/fi
#  5  fr-be          M  french-Belgium       europe/fr-be  (fr 8)
#  5  fr-fr          M  french               fr            (fr 5)
#  5  ga             -  irish-gaeilge        europe/ga
#  5  grc            M  greek-ancient        other/grc
#  5  hi             M  hindi                asia/hi
#  5  hr             M  croatian             europe/hr     (hbs 5)
#  5  hu             M  hungarian            europe/hu
#  5  hy             M  armenian             asia/hy
#  5  hy-west        M  armenian-west        asia/hy-west  (hy 8)
#  5  id             M  indonesian           asia/id
#  5  is             M  icelandic            europe/is
#  5  it             M  italian              europe/it
#  5  jbo            -  lojban               other/jbo
#  5  ka             -  georgian             asia/ka
#  5  kn             -  kannada              asia/kn
#  5  ku             M  kurdish              asia/ku
#  5  la             M  latin                other/la
#  5  lfn            M  lingua_franca_nova   other/lfn
#  5  lt             M  lithuanian           europe/lt
#  5  lv             M  latvian              europe/lv
#  5  mk             M  macedonian           europe/mk
#  5  ml             M  malayalam            asia/ml
#  5  ms             M  malay                asia/ms
#  5  ne             M  nepali               asia/ne
#  5  nl             M  dutch                europe/nl
#  5  no             M  norwegian            europe/no     (nb 5)
#  5  pa             -  punjabi              asia/pa
#  5  pl             M  polish               europe/pl
#  5  pt-br          M  brazil               pt            (pt 5)
#  5  pt-pt          M  portugal             europe/pt-pt  (pt 6)
#  5  ro             M  romanian             europe/ro
#  5  ru             M  russian              europe/ru
#  5  sk             M  slovak               europe/sk
#  5  sq             M  albanian             europe/sq
#  5  sr             M  serbian              europe/sr
#  5  sv             M  swedish              europe/sv
#  5  sw             M  swahili-test         other/sw
#  5  ta             M  tamil                asia/ta
#  5  tr             M  turkish              asia/tr
#  5  vi             M  vietnam              asia/vi
#  5  vi-hue         M  vietnam_hue          asia/vi-hue
#  5  vi-sgn         M  vietnam_sgn          asia/vi-sgn
#  5  zh             M  Mandarin             asia/zh
#  5  zh-yue         M  cantonese            asia/zh-yue   (yue 5)(zhy 5)
#


# Pty Language Age/Gender VoiceName          File          Other Languages
#  5  variant        F  female2              !v/f2
#  5  variant        F  female3              !v/f3
#  5  variant        F  female4              !v/f4
#  5  variant        F  female5              !v/f5
#  5  variant        F  female_whisper       !v/whisperf
#  5  variant        -  klatt                !v/klatt
#  5  variant        -  klatt2               !v/klatt2
#  5  variant        -  klatt3               !v/klatt3
#  5  variant        -  klatt4               !v/klatt4
#  5  variant        M  male2                !v/m2
#  5  variant        M  male3                !v/m3
#  5  variant        M  male4                !v/m4
#  5  variant        M  male5                !v/m5
#  5  variant        M  male6                !v/m6
#  5  variant        M  male7                !v/m7
#  5  variant        M  whisper              !v/whisper
#  5  variant      70F  female1              !v/f1
#  5  variant      70M  croak                !v/croak
#  5  variant      70M  male1                !v/m1
#



# from espeak import espeak
#
# espeak.set_voice("!v/f5")
#
# espeak.synth("Hi Cristian, Welcome on board, of your BMW !")
#
# while espeak.is_playing:
# 	pass


connection = obd.OBD()  # auto-connects to USB or RF port


def obd_speed():
    cmd = obd.commands.SPEED  # select an OBD command (sensor)

    response = connection.query(cmd)  # send the command, and parse the response

    print(response.value)  # returns unit-bearing values thanks to Pint
    print(response.value.to("mph"))  # user-friendly unit conversions

    return response.value.to("mph")
#http://python-obd.readthedocs.io/en/latest/Command%20Tables/

################ da spostare in classe esterna ############



# # Initiate video capture for video file
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

i = 0

import pandas as pd
output_data = [['filename','throttle_position', 'steering_angle','speed']]


while cap.isOpened() and i < 10000:
    i = i + 1
    time.sleep(.1)
    # Read first frame
    ret, frame = cap.read()

    filename = 'img/photo_' + str(i)  + '.jpg'
    print (filename)
    cv2.imwrite(filename,frame)
    throttle_position = 0
    steering_angle = 1
    speed = obd_speed()
    print (' speed')
    print (speed)
    output_data.append([filename,throttle_position, steering_angle, speed])


cap.release()
# out.release()
cv2.destroyAllWindows()
print output_data
df = pd.DataFrame(np.array(output_data))
df.to_csv("car_output_data.csv")

