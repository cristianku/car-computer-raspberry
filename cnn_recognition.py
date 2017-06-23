
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image

data_folder = 'traffic_signs/'

## reloading classifier from Json
# load json and create model
json_file = open(data_folder+ 'model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(data_folder + "model.h5")
print("Loaded model from disk")
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])



#########
test_image = image.load_img(data_folder+'speed_limit_80.ppm', target_size = (32, 32))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0) # add new dimension, corresponding to the batches


result = loaded_model.predict(test_image)
resultx =  result[0]

print (resultx)

# print result

# print loaded_model.predict_classes


# {'speed_limit_80'     : 3,
#  'traffic_light_green': 4,
#  'speed_limit_50'     : 2,
#  'speed_limit_30'     : 1,
#  'speed_limit_20'     : 0,
#  'traffic_light_red'  : 5}

if ( resultx[0] == 1):  prediction = 'speed_limit_20'
elif (resultx[1] == 1): prediction = 'speed_limit_30'
elif (resultx[2] == 1): prediction = 'speed_limit_50'
elif (resultx[3] == 1): prediction = 'speed_limit_80'
elif (resultx[4] == 1): prediction = 'traffic_light_green'
elif (resultx[5] == 1): prediction = 'traffic_light_red'


    # if (resultx > 0.8 ):
#      prediction = 'RED'
# else:
#      prediction = 'GREEN'
#
print " ****** "
print (" for image speed_limit_80.ppm , result = " + prediction)
print " ****** "
