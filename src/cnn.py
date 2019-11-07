import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical


def load_shoe_data(brand):
	shoe_data = pd.read_pickle(f'data/{brand}/resized_imgs.pkl')

	X_train, X_test, y_train, y_test = train_test_split(shoe_data['resize_img'], shoe_data['flip'])


	return X_train, X_test, y_train, y_test



