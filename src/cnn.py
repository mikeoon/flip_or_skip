import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical

'''
Begining code for the cnn

This was designed to make sure my images were being properly shaped
and in the correct format for Tensorflow

'''



def load_shoe_data(brand, nb_classes):
	shoe_data = pd.read_pickle(f'data/{brand}/resized_imgs.pkl')

	x_train, x_test, y_train, y_test = train_test_split(shoe_data['resize_img'], shoe_data['flip'])

	# Pandas DF into this array
	X_train = np.array([shoe for shoe in x_train])
	X_test = np.array([shoe for shoe in x_test])
	
	# Set to just two classes, flip or not
	Y_train = to_categorical(y_train, nb_classes)
	Y_test = to_categorical(y_test, nb_classes) 


	print('X_train shape:', X_train.shape)
	print(X_train.shape[0], 'train samples')
	print(X_test.shape[0], 'test samples')

	return X_train, X_test, Y_train, Y_test


def define_model(nb_filters, kernel_size, input_shape, pool_size):
    model = Sequential() 



    model.add(Conv2D(nb_filters, (kernel_size[0], kernel_size[1]),
                        padding='valid',
                        strides=(1,1), 
                        input_shape=input_shape,
                        data_format="channels_last")) #first conv. layer 
    model.add(Activation('relu'))

    model.add(Conv2D(nb_filters, (kernel_size[0], kernel_size[1]), padding='valid', data_format="channels_last")) #2nd conv. layer KEEP
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=pool_size, strides=(1,1))) 
    model.add(Dropout(0.5)) 

    model.add(Flatten()) 
    print('Model flattened out to ', model.output_shape)

    # now start a typical neural network
    model.add(Dense(32)) 
    model.add(Activation('relu'))

    model.add(Dropout(0.5)) 

    model.add(Dense(nb_classes)) 
    model.add(Activation('softmax')) 
    

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    return model

if __name__ == '__main__':
    batch_size = 100  
    nb_classes = 2   
    nb_epoch = 1     
    img_rows, img_cols = 500, 500  
    input_shape = (img_rows, img_cols, 3)  
    nb_filters = 28  
    pool_size = (2, 2) 
    kernel_size = (5, 5)

    X_train, X_test, Y_train, Y_test = load_shoe_data('nike', nb_classes)

    
    model = define_model(nb_filters, kernel_size, input_shape, pool_size)
    
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=nb_epoch,
            verbose=1, validation_data=(X_test, Y_test))

    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1]) # this is the one we care about
	