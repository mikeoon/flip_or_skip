import re
import requests
import json
import datetime as dt
from numpy import nan
from bs4 import BeautifulSoup


goat_url = 'https://www.goat.com/sneakers/air-jordan-12-retro-reverse-taxi-130690-017'

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'}
r = requests.get(goat_url, headers=headers)

soup = BeautifulSoup(r.content, 'lxml')

test = soup.find_all('script', {'type': 'application/ld+json'})

json_lst = []
for t in test:
	json_lst.append(json.loads(t.text))

# Scrapes only sku number to link back to OG shoe from stockx scrape
# and the silhoutte
print(json_lst[1]['itemListElement'][-1]['item']['name'])
print(json_lst[0]['sku'])