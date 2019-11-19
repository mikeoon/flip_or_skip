import numpy as np
import pandas as pd

import clean_scrape as cs
import shoe_pipeline as sp

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix


def print_confusion_mat(tn, fp, fn, tp):
	'''
	Prints the confusion matrix of a model's prediction

	returns None
	'''
    print(f'True Negatives: {tn}  | True Positives: {tp}')
    print(f'False Negatives: {fn} | False Positives: {fp}')


def create_model_df(brand):
	'''
	Creates the dataframe for the model
	All rows in the dataframe can be fed into the model
	Splits up the data into X, y

	X = current model features accepted by model
	y = targets (flip or not)

	returns X and y
	''' 

	df = cs.combine_shoe_pkls(brand)
	X, y = sp.flip_skip_pipeline(df, brand)

	return X, y


def create_flipskip_rfc(X, y, brand):
	'''
	Creates RandomForestCalssifier Models for nike and air_jordan
	Fits the model with the given X and y, will train test split

	Returns the fit RandomForestClassifier and the X_test and y_test that go along
	'''

	if brand == 'nike':
		rfc = RandomForestClassifier(max_depth=17.0, n_estimators=50)
	elif brand =='air_jordan':
		rfc = RandomForestClassifier(criterion='entropy',max_depth= 19.0, n_estimators=100)

	X_train, X_test, y_train, y_test = train_test_split(X, y)

	rfc.fit(X_train, y_train)

	return rfc, X_test, y_test
