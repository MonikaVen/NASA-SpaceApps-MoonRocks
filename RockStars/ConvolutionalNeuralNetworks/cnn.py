# Convolutional Neural Network

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

img_size = 256
# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(128, (3, 3), input_shape = (img_size, img_size, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second and third convolutional layer
classifier.add(Conv2D(128, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
classifier.add(Conv2D(128, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = img_size, activation = 'relu'))
classifier.add(Dense(units = 3, activation = 'softmax'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (img_size, img_size),
                                                 batch_size = 10,
                                                 )

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (img_size, img_size),
                                            batch_size = 20,
                                            )

classifier.fit_generator(training_set,
                         steps_per_epoch = 50,
                         epochs = 10,
                         validation_data = test_set,
                         validation_steps = 80)

# Part 3 - Making new predictions

import numpy as np
from keras.preprocessing import image
test_image_1 = image.load_img('dataset/single_prediction/breccia.jpg', target_size = (img_size, img_size))
test_image_2 = image.load_img('dataset/single_prediction/anorthite.jpg', target_size = (img_size, img_size))
test_image_3 = image.load_img('dataset/single_prediction/basalt.jpg', target_size = (img_size, img_size))
test_image_1 = image.img_to_array(test_image_1)
test_image_1 = np.expand_dims(test_image_1, axis = 0)
test_image_2 = image.img_to_array(test_image_2)
test_image_2 = np.expand_dims(test_image_2, axis = 0)
test_image_3 = image.img_to_array(test_image_3)
test_image_3 = np.expand_dims(test_image_3, axis = 0)
result_1 = classifier.predict(test_image_1)
result_2 = classifier.predict(test_image_2)
result_3 = classifier.predict(test_image_3)
index_info = training_set.class_indices
print(index_info)

results = [result_1, result_2, result_3]
print(results)
for result in results:
    if result[0][0] == 1:
        prediction = 'Anorthite'
        print(prediction)
    elif result[0][1] == 1:
        prediction = 'Basalt'
        print(prediction)
    elif result[0][2] == 1:
        prediction = 'Breccia'
        print(prediction)

# elif result[0][3] == 1:
#     prediction = 'elephant'

classifier.save('../ServeModel/models/model')
classifier.save_weights("model_512.h5")
# serialize model to JSON
# model_json = classifier.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# 
# print("Saved model to disk")