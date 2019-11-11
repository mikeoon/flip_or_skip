import pandas as pd
import numpy as np
import pickle
from skimage import io, transform




def _dummy_colors(df, mcolor=True, ncolor=True, num_colors=1):
	if mcolor:
		u_m_colors = df['m_color'].unique()
		
		for c in u_m_colors:
			df['m_color_'+c] = (df['m_color'] == c) * 1
	
	if ncolor:
		for i in range(num_colors):
			u_color = df[f'color_{i}'].unique()
			for c in u_color:
				if type(c) != type(1.0):
					df[f'color_{i}_'+(c.replace(' ','_').strip())] = (df[f'color_{i}'] == c) *1
	
	return df

# Dummys the cuts 
def _dummy_cut(df):
	cuts = df['cut'].unique()
	for c in cuts:
		if c != 0:
			df[f'cut_{c}'] = (df['cut'] == c) * 1
	return df


def _dummy_release_date(df):
	df['release_day'] = [-1 if d is None else d.weekday() for d in df['release_date']]
	# Days are released by 0 - 6, 0 = monday
	for i in range(7):
		df[f'release_{i}'] = (df['release_day'] == i)*1

	return df.drop('release_day', axis=1, inplace=True)


def _dummy_silhouette(df, brand):
	if brand == 'nike':
		styles = set(['max 97','max 95', 'max 720', 'max 270', 'react', 'presto', 'lebron', 'kobe', 'vapormax', 'kyrie', 
               'pg','air force 1', 'sb', 'sb dunk', 'blazer', 'kd', 'foamposite', 'tailwind', 'cortez', 
               'adapt', 'huarache'])
	elif brand == 'air_jordan':
		styles = styles_ = set(['jordan '+ str(i) for i in range(1, 20)] + ['xxx', 'xxx1', 'xxxii', 'xxxiii'])

	for s in styles:
		df[brand +f'_{s}'] = [1 if s in name else 0 for name in df['name']]

	return df


# Hard coded, this is for my first model to clean up patchy data
def _patch_up_m_color(df, brand):
	if brand == 'nike':
		df.loc[91, 'm_color'] = 'red'
		df.loc[128, 'm_color'] = 'multi-color'
		df.loc[215, 'm_color'] = 'teal tint'
		df.loc[419, 'm_color'] = 'black'
		df.loc[437, 'm_color'] = 'black'
		df.loc[503, 'm_color'] = 'white pure platinum'
		df.loc[987, 'm_color'] = 'cinncinati reds'
	elif brand == 'air_jordan':
		df.loc[110, 'm_color'] = 'hyper blue'
		df.loc[110, 'color_0'] = 'electro orange'
		df.loc[110, 'color_1'] = 'black'
		df.loc[794, 'm_color'] = 'copper'
		df.loc[794, 'color_0'] = 'black'
		df.loc[794, 'color_1'] = 'white'
		df.loc[934, 'm_color'] = 'black'
		df.loc[979, 'm_color'] = 'white'
		df.loc[979, 'color_0'] = 'yellow'
		df.loc[979, 'color_1'] = 'gum'

	return df

def create_img_df(df):
	image_df = df[['name', 'flip']].copy()
	image_df['img']=[name.replace(' ', '_')+f'_img01.jpg' for name in df['name']]
	return image_df

def pkle_img(df, brand):
	df['resize_img'] = [transform.resize(io.imread('data/nike/'+shoe), (500, 500, 3)) for shoe in df['img']]
	with open(f'data/{brand}/resized_imgs.pkl', 'wb') as f:
		pickle.dump(df, f)



def flip_skip_pipeline(df, brand, num_c=2):
	
	if brand == 'nike':
		X_cols = ['name', 'cut', 'retail_price', 'm_color', 'color_0', 'color_1', 'release_date']
	elif brand =='air_jordan':
		X_cols = ['name', 'cut', 'retail_price','retro', 'm_color', 'color_0', 'color_1', 'release_date']
	target = ['flip']
	drop_cols = ['name', 'cut', 'm_color', 'color_0', 'color_1', 'release_date']
	
	model_df = df[X_cols].copy()
	model_targets = df['flip'].copy() * 1
	_patch_up_m_color(model_df, brand)
	_dummy_colors(model_df, num_colors=num_c)
	_dummy_cut(model_df)
	_dummy_release_date(model_df)
	_dummy_silhouette(model_df, brand)

	return model_df.drop(drop_cols, axis=1), model_targets








