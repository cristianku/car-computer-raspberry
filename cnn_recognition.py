
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
test_image = image.load_img(data_folder+'other.png', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0) # add new dimension, corresponding to the batches

result = loaded_model.predict(test_image)
resultx =  result[0]

# print (resultx)

# print result

# print loaded_model.predict_classes

# {'traffic_other': 2, 'traffic_light_green': 0, 'traffic_light_red': 1}


if ( resultx[0] == 1):
    prediction = 'traffic_light_green'
elif ( resultx[1] == 1):
    prediction = 'traffic_light_red'
elif (resultx[2] == 1):
    prediction = 'traffic_other'


    # if (resultx > 0.8 ):
#      prediction = 'RED'
# else:
#      prediction = 'GREEN'
#
print " ****** "
print (" for image other.png , result = " + prediction)
print " ****** "
