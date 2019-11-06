import pandas as pd
import numpy as np


def get_image01_paths(df):
	return [name.replace(' ', '_')+'_img01.jpg' for name in df['name']]




def dummy_colors(df, mcolor=True, num_colors=1):
	u_m_colors = df['true_m_color'].unique()
	
	for c in u_m_colors:
		df['m_color_'+c] = (df['true_m_color'] == c) * 1
	

	for i in range(,num_colors):
		u_color = df[f'color_{i}'].unique()
		for c in u_color:
			if type(c) != type(1.0):
				df[f'color_{i}_'+(c.replace(' ','_'))] = (df[f'color_{i}'] == c) *1
	
	return df

def patch_up_m_color(df, brand):
	if brand == 'nike':
		df.loc[91, 'true_m_color'] = 'red'
		df.loc[128, 'true_m_color'] = 'multi-color'
		df.loc[215, 'true_m_color'] = 'teal tint'
		df.loc[419, 'true_m_color'] = 'black'
		df.loc[437, 'true_m_color'] = 'black'
		df.loc[503, 'true_m_color'] = 'white pure platinum'
		df.loc[987, 'true_m_color'] = 'cinncinati reds'
	elif brand ==' air_jordan':
		print('THIS IS NOT IMPLEMENTED YET')






