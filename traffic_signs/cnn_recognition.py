
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
from keras.models import load_model



data_folder = ''

## reloading classifier from Json
# load json and create model
# json_file = open(data_folder+ 'model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# load weights into new model
model = load_model('model.h5')
print("Loaded model from disk")



#########
test_image = image.load_img(data_folder+'green_light.png', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0) # add new dimension, corresponding to the batches
print test_image

print model.predict(test_image)

# print result

# print loaded_model.predict_classes

# {'speed_limit_80': 7, 'speed_limit_100': 0, 'speed_limit_60': 5, 'speed_limit_70': 6, 'speed_limit_120': 1, 'traffic_light_green': 9, 'speed_limit_50': 4, 'speed_limit_80_end': 8, 'speed_limit_30': 3, 'speed_limit_20': 2, 'traffic_light_red': 10}

prediction = ""
# if ( resultx[0] == 1):  prediction = 'speed_limit_20'
# elif (resultx[1] == 1): prediction = 'speed_limit_30'
# elif (resultx[2] == 1): prediction = 'speed_limit_50'
# elif (resultx[3] == 1): prediction = 'speed_limit_80'
# elif (resultx[4] == 1): prediction = 'traffic_light_green'
# elif (resultx[5] == 1): prediction = 'traffic_light_red'


    # if (resultx > 0.8 ):
#      prediction = 'RED'
# else:
#      prediction = 'GREEN'
#
# print " ****** "
# print (" PREDICTION  , result = " + prediction)
# print " ****** "
