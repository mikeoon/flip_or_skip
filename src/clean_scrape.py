import pandas as pd
import numpy as np
import glob
import re




def combine_shoe_pkls(brand):
	'''
	Takes in a brand [nike, air_jordan]
	
	Pickles all shoes together into one dataframe

	returns such data frame for the specified brand

	'''

	pathname = f'data/{brand}/shoe_details/*.pkl'
	shoe_pkls = glob.iglob(pathname)
	shoe_rows = [pd.read_pickle(shoe) for shoe in shoe_pkls]

	df = pd.concat(shoe_rows, axis=0, sort=True)
	df = df.drop(['color_5','sku'], axis=1)
	df = df.rename(columns={'avg_sale': 'avg_resale'}).sort_index()
	df = df.sort_index()

	df = _remove_child_shoes(df)
	df = _remove_duplicate_shoes(df)
	df = _remove_missing_resale(df)
	df = _remove_missing_retail(df)
	df = _fix_types(df)
	df = _fix_m_color(df, brand)
	df = _add_columns(df)


	return df


def _remove_duplicate_shoes(df):
	'''
	removes duplicate shoes from the data frame

	returns df with duplicates removed
	'''

	duplicates = set()
	dup_shoes = []
	for i, shoe in df.iterrows():
		if shoe['name'] not in duplicates:
			duplicates.add(shoe['name'])
		else:
			df.drop(i, axis=0, inplace=True)
	return df


def _remove_missing_resale(df):
	'''
	Some sneakers have missing resale values

	Removes such shoes

	returns dataframe

	'''
	no_avg = df[df['avg_resale'].isnull()].index
	return df.drop(index=no_avg)


def _remove_missing_retail(df):
	'''
	Some sneakers have missing retail values

	Removes such shoes

	returns dataframe

	'''
	no_retail = df[df['retail_price'].isnull()].index
	return df.drop(index=no_retail)


def _remove_child_shoes(df):

	'''
	Removes all childrends shoes
	[td, ps, gs]

	returns dataframe

	'''
	pattern = re.compile("\((td|ps|gs)\)")
	for i,shoe in df.iterrows():
		if pattern.search(shoe['name'].lower()):
			df.drop(i, axis=0, inplace=True)
	return df


def _fix_types(df):
	'''
	Fixes types of data points to floats and ints

	return dataframe

	'''
	df['avg_resale'] = df['avg_resale'].map(lambda x: float(x))
	df['retail_price'] = df['retail_price'].map(lambda x: float(x))
	df['num_sales'] = df['num_sales'].map(lambda x: int(x))
	return df


def _fix_m_color(df, brand):
	'''
	input brands [nike, air_jordan]
	Some m_colors in the initial scrape can come out incomplete
	Running the rescrape on the scrape_sx.py file will fix this

	Function will replace all m_color colum with correctly scraped values
	Found in pickled files

	returns df

	'''
	pathname = f'data/{brand}/m_color/*.pkl'
	color_pkls = glob.iglob(pathname)
	color_rows = [pd.read_pickle(shoe) for shoe in color_pkls]
	df = df.drop('m_color', axis=1)
	color_df = pd.concat(color_rows, sort=True)
	color_df = color_df.set_index('name')
	return df.join(color_df, on='name')



def _add_columns(df, threshold=0):
	'''
	add target flip column
	net_gain column
	net_profit column

	returns dataframe
	'''
	df['net_gain'] = df['avg_resale'] - df['retail_price']
	df['net_profit'] = (df['avg_resale'] - (df['avg_resale'] * 0.125)) - df['retail_price']
	df['flip'] = df['net_profit'] > threshold
	return df









