import pandas as pd
import numpy as np
import glob



def combine_shoe_pkls(brand):
	pathname = f'data/{brand}/shoe_details/*.pkl'
	shoe_pkls = glob.iglob(pathname)
	shoe_rows = [pd.read_pickle(shoe) for shoe in shoe_pkls]

	df = pd.concat(shoe_rows, axis=0, sort=True)
	df = df.drop(['color_5','sku'], axis=1)
	df = df.rename(columns={'avg_sale': 'avg_resale'}).sort_index()
	df = df.sort_index()

	df = _remove_duplicate_shoes(df)
	df = _remove_missing_resale(df)

	return df


def _remove_duplicate_shoes(df):
	duplicates = set()
	dup_shoes = []
	for i, shoe in df.iterrows():
		if shoe['name'] not in duplicates:
			duplicates.add(shoe['name'])
		else:
			df.drop(i, axis=0, inplace=True)
	return df

def _remove_missing_resale(df):
	no_avg = df[df['avg_resale'].isnull()].index
	return df.drop(index=no_avg, inplace=True)








