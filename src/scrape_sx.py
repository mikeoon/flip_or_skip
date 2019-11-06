import requests
import pickle
import boto3
import datetime as dt
import pandas as pd

from random import randint
from time import sleep
from numpy import nan
from bs4 import BeautifulSoup



def _scrape_shoe(stockx_url, color_count, headers, brand):
	r = requests.get(stockx_url, headers=headers)
	img_files = []

	print(r)

	soup = BeautifulSoup(r.content, 'lxml')


	detail_info = {'name': None,'sku':None, 'style': None, 'm_color': None, 'retail_price': None, 
				'release_date': None, 'num_sales': None, 'avg_sale': None}

	# shoe name
	shoe_name = soup.find('h1',{'class':'name'})
	while shoe_name == None:
		print('Sorry, slight hold up')
		r = requests.get(stockx_url, headers=headers)
		soup = BeautifulSoup(r.content, 'lxml')
		shoe_name = soup.find('h1',{'class':'name'})


	detail_info, s_name = _ft_from_name(shoe_name.text.lower().replace('/', '_'), detail_info)

	print(f'Begin Scrape of {s_name}:')

	s_name = '_'.join(s_name.split())
	# get image(s) of shoe
	# if stockx has 360 images, then it grabs all for that shoe
	# if not, just the one


	img_area = soup.find('div',{'class':'image-container'})
	if img_area == None:
		img_area = soup.find('div', {'class': 'product-media'}).find('img')
	else:
		img_area = img_area.find('img')
	
	img_url = img_area['src']
	s3 = boto3.client('s3')
	if '-360.img' in img_url:
		img360 = True
		# downloads imgs of shoes in jpg format from
		# urls scraped from stockx
		for n in range(1, 37):
			# broken up here to handle the img url names
			if n <10:
				r2 = requests.get(img_url.replace('img01', f'img0{n}'), allow_redirects=True)
				open(f'data/{brand}/{s_name}_img0{n}.jpg', 'wb').write(r2.content)
				local_file_name = f'data/{brand}/{s_name}_img0{n}.jpg'
			else:
				r2 = requests.get(img_url.replace('img01', f'img{n}'), allow_redirects=True)
				open(f'data/{brand}/{s_name}_img{n}.jpg', 'wb').write(r2.content)
				local_file_name = f'data/{brand}/{s_name}_img{n}.jpg'
			print(f'Downloaded image of  {n}')
			bucket_name = 'mikeoon-galvanize-bucket'
			s3.upload_file(Filename=local_file_name, 
		    	           Bucket=bucket_name, 
		        	       Key=local_file_name)
			img_files.append(local_file_name)
	else:
		print(f'No 360 images, just the one for {s_name}')
		img360 = False
		r2 = requests.get(img_url, allow_redirects=True)
		open(f'data/{brand}/{s_name}_img01.jpg', 'wb').write(r2.content)
		local_file_name = f'data/{brand}/{s_name}_img01.jpg'
		bucket_name = 'mikeoon-galvanize-bucket'
		s3.upload_file(Filename=local_file_name, 
	    	           Bucket=bucket_name, 
	        	       Key=local_file_name)
		img_files.append(local_file_name)
	
	print('Done with images')
	detail_info['img360'] = img360

	# gets details style, colorway, retail price, release date
	detail_table = soup.find_all('div', {'class':'detail'})

	for i in detail_table:
		d = i.text.lower().strip().split(' ')
		# Breaks down the string into parts so better store data
		if d[0] == 'retail':
			detail_info['retail_price'] = float(d[2][1:].replace(',', ''))
		elif d[0] == 'release':
			temp = [int(t) for t in d[2].split('/')]
			detail_info['release_date'] = dt.date(temp[2], temp[0], temp[1])
		elif d[0] == 'colorway':
			colors = i.text.lower().split('/')
			if len(colors) > 1:
				detail_info['m_color'] = colors[0].replace('colorway', '').strip()
				cc = 0
				for i, c in enumerate(colors[1].split('-')):
					detail_info[f'color_{i}'] = c
					cc+=1
			else:
				colors = i.text.lower().split()
				detail_info['m_color'] = colors[0].replace('colorway', '').strip()
				cc = 0
				for i, c in enumerate(colors[2:]):
					print(c)
					detail_info[f'color_{i}'] = c
					cc+=1

			# Updates the color_{number} feature count to fill in later for df
			if cc > color_count:
				color_count = cc
		else:
			detail_info[d[0]] = d[1]


	# gets gauge table, num sales, price premium, avg sale price
	gauge_table = soup.find_all('div', {'class':'gauge-container'})

	for i in gauge_table:
		d = i.text.lower().strip()
		if '#' in d:
			if d[10:] == '--':
				detail_info['num_sales'] = nan
			else:
				detail_info['num_sales'] = int(d[10:])
		elif '$' in d:
			if d[19:] == '--':
				detail_info['avg_sale'] = nan
			else:
				detail_info['avg_sale'] = float(d[19:].replace(',', ''))

	return _color_fill(detail_info, cc), color_count


# Only used if the m_colors in the above code fails
def _re_scrape_color(url):
	r = requests.get(url, headers=headers)
	img_files = []

	print(r)

	soup = BeautifulSoup(r.content, 'lxml')
	shoe_name = soup.find('h1',{'class':'name'})

	while shoe_name == None:
		print('Sorry, slight hold up')
		sleep(randint(2, 4))
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.content, 'lxml')
		shoe_name = soup.find('h1',{'class':'name'})
	shoe_name = shoe_name.text.lower().replace('/', '_')

	shoe_colors = {'name':shoe_name}

	detail_table = soup.find_all('div', {'class':'detail'})
	for i in detail_table:
		d = i.text.lower().strip().split(' ')
		if d[0] == 'colorway':
			colors = i.text.lower().split('/')
			if len(colors) > 1:
				shoe_colors['m_color'] = colors[0].replace('colorway', '').strip()

	return shoe_colors

# Scrapes all urls for jordan shoes that are on StockX
# pickles it or just returns a list if one doesn't want the pickle
def _scrape_shoe_pgs(url, headers, brand, p=True):
	attach = []
	for pg in range(1, 26):
		s_url = url + f'?page={pg}'
		r = requests.get(s_url, headers=headers)
		print(r)
		print(s_url)

		soup = BeautifulSoup(r.content, 'lxml')
		shoe_pgs = soup.find_all('div', {'class':'tile browse-tile'})
		for shoe in shoe_pgs:
			if '--' not in shoe.find('div', {'class':'price-line-div'}).text:
				attach.append(shoe.find('a')['href'])
	if p:
		with open(f'data/{brand}/stockx_urls.pkl', 'wb') as f:
			pickle.dump(attach, f)
	else:
		return attach



# If a shoe doesn't have that many colors
# nans are filled into extra color rows to keep shape of database
def _color_fill(detail_info, cc):
	while cc < color_count:
		cc+=1
		detail_info[f'color_{cc}'] = nan
	return detail_info

# Creates features from the name of the shoe
# Returns the name of the shoe as well
def _ft_from_name(s_name, detail_info):
	detail_info['name'] = s_name
	if 'retro' in s_name:
		detail_info['retro'] = 1
	else:
		detail_info['retro'] = 0

	if 'high' in s_name:
		detail_info['cut'] = 3
	elif 'mid' in s_name:
		detail_info['cut'] = 2
	elif 'low' in s_name:
		detail_info['cut'] = 1
	else:
		detail_info['cut'] = 0

	return detail_info, s_name





if __name__ == '__main__':
	color_count = 5
	shoe_brand_urls = {'air_jordan':'https://stockx.com/retro-jordans', 
						'nike':'https://stockx.com/nike'}
	# will get 403 response without this
	headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'}
	#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0'}
	base_url = 'https://stockx.com'
	
	# For tests
	#stockx_url =  ['https://stockx.com/air-jordan-6-retro-travis-scott']


	print('\nHello! what shoe brand do you want?\n [air_jordan, nike]?')
	brand = input()
	print('Do you want to get pgs or scrape shoes?(pg/sh)')
	pg_sh = input()
	if pg_sh.lower() == 'pg':
		_scrape_shoe_pgs(shoe_brand_urls[brand], headers, brand)

	else:
		print('Scrape, Great. Is it pickled already?(y/n)')
		r_pickle = input()
		if r_pickle.lower() == 'y':
			from_pkl = True
		else:
			from_pkl = False

		if from_pkl:
			with open(f'data/{brand}/stockx_urls.pkl', 'rb') as file:
				stockx_urls = pickle.load(file)
		else:
			stockx_urls = _scrape_shoe_pgs(shoe_brand_urls[brand], headers, brand, p=False)


	# if it breaks, need to update the i as well to whatever the base is
	# can't get shoe 116... need to figure out why
	stop_point = 0
	for i, url in enumerate(stockx_urls[stop_point:]):
		shoe_info, color_count = _scrape_shoe(base_url+url, color_count, headers, brand)
		new_shoe = pd.DataFrame(shoe_info, index=[i+stop_point])
		print('pickling shoe information')

		new_shoe.to_pickle(f'data/{brand}/shoe_details/shoe{i+stop_point}.pkl')
		print(f'Done with shoe {i+stop_point} in pickled list\n')
	
	'''
	# To rescrape colors, m_colors in main df
	redo_colors = []
	for i, url in enumerate(stockx_urls[stop_point:]):
		row = _re_scrape_color(base_url+url)
		print(row)
		new_color = pd.DataFrame(row, index=[i+stop_point])
		new_color.to_pickle(f'data/{brand}/m_color/shoe{i+stop_point}.pkl')

		sleep(randint(2, 4))

		print(f'Done with shoe{i+stop_point}')
		print()
	'''





