import re
import requests
from bs4 import BeautifulSoup


stockx_url = 'https://stockx.com/air-jordan-10-retro-seattle'
# will get 403 response without this
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'}



r = requests.get(stockx_url, headers=headers)

soup = BeautifulSoup(r.content, 'lxml')

# shoe name
shoe_name = soup.find('h1',{'class':'name'})
print(shoe_name.text)

# gets details style, colorway, retail price, release date
# NOT CLEANED YET
detail_table = soup.find_all('div', {'class':'detail'})
details = []
for i in detail_table:
	details.append(i.text.split(' '))


# gets gauge table, num sales, price premium, avg sale price
# NOT CLEANED YET
gauge_table = soup.find_all('div', {'class':'gauge-container'})
gauges = []
for i in gauge_table:
	gauges.append(i.text.split('$'))




# to test

for d in details:
	print(d)


for g in gauges:
	print(g)








