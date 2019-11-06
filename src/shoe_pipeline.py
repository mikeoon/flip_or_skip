import pandas as pd
import numpy as np


def get_image_paths(df, num=1):
	return [name.replace(' ', '_')+f'_img0{i}.jpg' for name in df['name']]




def dummy_colors(df, mcolor=True, ncolor=True, num_colors=1):
	if mcolor:
		u_m_colors = df['m_color'].unique()
		
		for c in u_m_colors:
			df['m_color_'+c] = (df['m_color'] == c) * 1
	
	if ncolor:
		for i in range(num_colors):
			u_color = df[f'color_{i}'].unique()
			for c in u_color:
				if type(c) != type(1.0):
					df[f'color_{i}_'+(c.replace(' ','_'))] = (df[f'color_{i}'] == c) *1
	
	return df

# Dummys the cuts 
def dummy_cut(df):
	cuts = df['cut'].unique()
	for c in cuts:
		if c != 0:
			df[f'cut_{c}'] = (df['cut'] == c) * 1
	return df

# Hard coded, this is for my first model to clean up patchy data
def patch_up_m_color(df, brand):
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






