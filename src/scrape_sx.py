import re
import requests
import datetime as dt
from numpy import nan
from bs4 import BeautifulSoup


def _scrape_shoe(stockx_url, color_count, headers):
	r = requests.get(stockx_url, headers=headers)

	print(r)

	soup = BeautifulSoup(r.content, 'lxml')
	detail_info = {'name': None,'sku':None, 'style': None, 'm_color': None, 'retail_price': None, 
				'release_date': None, 'num_sales': None, 'avg_sale': None}

	# shoe name
	# Need to think of a way to get the name cleaned up into Brand, is it a retro?, actual name
	shoe_name = soup.find('h1',{'class':'name'})
	detail_info = _ft_from_name(shoe_name.text.lower(), detail_info)

	# gets details style, colorway, retail price, release date
	# Clean but need to handle the colors
	detail_table = soup.find_all('div', {'class':'detail'})

	for i in detail_table:
		d = i.text.lower().strip().split(' ')
		# Breaks down the string into parts so better store data
		if d[0] == 'retail':
			detail_info['retail_price'] = float(d[2][1:])
		elif d[0] == 'release':
			temp = [int(t) for t in d[2].split('/')]
			detail_info['release_date'] = dt.date(temp[2], temp[0], temp[1])
		elif d[0] == 'colorway':
			colors = i.text.lower().split('/')
			detail_info['m_color'] = colors[0].split(' ')[1]
			cc = 0
			for i, c in enumerate(colors[1].split('-')):
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
			detail_info['num_sales'] = int(d[10:])
		elif '$' in d:
			detail_info['avg_sale'] = float(d[19:])

	return _color_fill(detail_info, cc), color_count


def _scrape_shoe_pgs(url, headers):
	attach = []
	for p in range(1, 26):
		s_url = url + f'?page={p}'
		r = requests.get(stockx_url, headers=headers)
		print(r)

		soup = BeautifulSoup(r.content, 'lxml')
		shoe_pgs = soup.find_all('div', {'class':'tile browse-tile'})
		for shoe in shoe_pgs:
			if '--' not in shoe.find('div', {'class':'price-line-div'}).text:
				attach.append(shoe.find('a')['href'])
	return attach




def _color_fill(detail_info, cc):
	while cc < color_count:
		cc+=1
		detail_info[f'color_{cc}'] = nan
	return detail_info


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

	return detail_info





# to test
color_count = 4

#stockx_url = 'https://stockx.com/retro-jordans'
stockx_url = ['https://stockx.com/air-jordan-10-retro-seattle','https://stockx.com/air-jordan-1-retro-high-unc-leather']
#stockx_url =  'https://stockx.com/air-jordan-1-retro-high-unc-leather'
# will get 403 response without this
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'}

base_url = 'https://stockx.com'
#print(_scrape_shoe_pgs(stockx_url, headers))
for url in stockx_url:
	shoe_info, color_count = _scrape_shoe(url, color_count, headers)

	for k,v in shoe_info.items():
		print(f'{k} = {v}')






