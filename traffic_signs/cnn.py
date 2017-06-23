import os
#
# print (" ########### " )
# print (" os.curdir = " + os.curdir)
# print (" ########### ")
# exit()
#
# print (os.listdir(os.curdir))
#
# print (os.listdir('/dataset'))

if os.path.exists('/traffic_signs'):
    data_folder = '/traffic_signs/'
else:
    data_folder = ''

if os.path.exists('/output'):
    output_folder = '/output/'
else:
    output_folder = ''


print (" ********* "   )
print (" ********* "   )
print ("data folder: "  + data_folder )
print (" ********* "   )

from keras.models import  Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense, Dropout


# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#Initializing CNN

classifier = Sequential()


# Step 1 - Convolution
#  number of feature detectors,, kerne size
# feature detectors = 32
# size of filter kernel = 3
classifier.add(Convolution2D(32,3,3,input_shape=(64,64,3), activation='relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2,2)))
#
###################
# adding second convolutional layer
# increase feature detectors to 64
classifier.add(Convolution2D(64,3,3, activation='relu'))
# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2,2)))
###################



# Step 3 - Flattening
classifier.add(Flatten ())

# Step 4 - Full connection
classifier.add(Dense(output_dim = 128,activation= 'relu'))

classifier.add(Dropout(0.5))

classifier.add(Dense(units = 11,activation= 'softmax')) # --> probability softmax computation

classifier.compile(optimizer='adam', loss ='categorical_crossentropy', metrics=['accuracy'])

print classifier.summary()

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

# IMAGE augmentation


# rescaling between 0 and 1 + transformations ## many different batches with RANDOM shifts, rotations, etc....
train_datagen   = ImageDataGenerator(
                                    rescale=1. / 255,
                                    shear_range=0.2, #geometrical transformation
                                    zoom_range=0.2,
                                    horizontal_flip=True)
print
# batches creation
training_set = train_datagen.flow_from_directory(data_folder + 'training_set',
                                                 target_size=(64, 64),  # this dimension should be same as Convolution Layer
                                                                        # classifier.add(Convolution2D(32,3,3,
                                                                        # input_shape=(64,64,3), activation='relu'))
                                                 batch_size=32,
                                                 class_mode='categorical')

print training_set
# printing the classification
print (" ################# " )
print (" ################# " )
print (" ################# " )
print (training_set.class_indices)
print (" ################# " )
print (" ################# " )
print (" ################# " )


# TEST SET AUGMENTATION

# rescaling between 0 and 1
test_datagen    = ImageDataGenerator(rescale=1. / 255)

# batches creation
test_set        = test_datagen.flow_from_directory(data_folder + 'test_set',
                                                    target_size=(64, 64),
                                                    batch_size=32,
                                                   class_mode='categorical')
# printing the classification
print (" ################# ")
print (" ################# ")
print (" ################# ")
print (test_set.class_indices)
print (" ################# ")
print (" ################# ")
print (" ################# ")
# Fitting the Model
#


classifier.fit_generator(
                    training_set,
                    steps_per_epoch=30,      # number of images per epochs ( per batch )
                    epochs=5                #Total number of steps (batches of samples)
                                              # to yield from generator before declaring one epoch
                                              # finished and starting the next epoch.
                                              # It should typically be equal to the number of unique samples
                                              # of your dataset divided by the batch size.

                    validation_data=test_set, #validation_data: This can be either
                    #                           #  A generator
                    #                           # for the validation data
                    #                           # A tuple (inputs, targets)
                    #                           # A tuple (inputs, targets, sample_weights).
                    validation_steps=20       # number of images per epochs ( per batch )
                    )

print (" ########### ")
print (" ########### ")
print (" ########### ")
print (" saving model to " + output_folder + "model.json")
print (" ########### ")
print (" ########### ")
print (" ########### ")
print (" ########### ")
# serialize model to JSON
# model_json = classifier.to_json()
# with open(output_folder + "model.json", "w") as json_file:
#     json_file.write(model_json)
# serialize weights to HDF5
classifier.save(output_folder + "model.h5")
print("Saved model to disk")


