
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
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])



#########
test_image = image.load_img(data_folder+'green_light.png', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0) # add new dimension, corresponding to the batches

result = loaded_model.predict(test_image)
resultx =  result[0][0]
print (resultx)
if (resultx > 0.8 ):
     prediction = 'RED'
else:
     prediction = 'GREEN'

print (" for image green_light.png , result = " + prediction)