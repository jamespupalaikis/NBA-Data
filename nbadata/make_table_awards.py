import pandas as pd
import os
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup



def make_accolades_table(save = True):
	url = 'https://www.basketball-reference.com/awards/mvp.html'
	url2 = 'https://www.basketball-reference.com/awards/dpoy.html'
	html = urlopen(url)
	html2 = urlopen(url2)
	soup = BeautifulSoup(html)
	soup2 = BeautifulSoup(html2)
	g = (soup.find(id = 'mvp_NBA'))
	g2 = (soup2.find(id = 'dpoy_NBA'))
	mvps = []
	dpoys = []

	table_rows = g.find_all('tr')

	for tr in table_rows:
		td = tr.find_all('td')
		#print(type(td))
		row = [i.text for i in td ]
		mvps.append(row[1:2])

	table_rows2 = g2.find_all('tr')

	for tr in table_rows2:
		td = tr.find_all('td')
		row = [i.text for i in td]
		dpoys.append(row[1:2])

	mvps = list(filter(lambda x: (x != []), mvps))
	dpoys = list(filter(lambda x: (x != []), dpoys))
	mvps += [['N/A'] for i in range(6)]

	dpoys += [['N/A'] for i in range(33)]
	dpoys = [i for [i] in dpoys]

	mvplist = pd.DataFrame(mvps[::-1])

	mvplist['DPOY'] = dpoys[::-1]
	mvplist['Year'] = range(1950,2021)
	mvplist = mvplist.rename(columns = {0 : 'MVP'})
	if (save):
		mvplist.to_csv('raw_data/%ito%iaccolades.csv' %(1950,2020))
	return mvplist

make_accolades_table()