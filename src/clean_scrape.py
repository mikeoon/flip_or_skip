import pandas as pd
import numpy as np
import glob



def combine_shoe_pkls(brand):
	pathname = f'data/{brand}/shoe_details/*.pkl'
	shoe_pkls = glob.iglob(pathname)
	shoe_rows = [pd.read_pickle(shoe) for shoe in shoe_pkls]

	df = pd.concat(shoe_rows, axis=0, sort=True)
	df = df.drop('color_5', axis=1)
	df = df.drop('sku', axis=1)
	return df.sort_index()









