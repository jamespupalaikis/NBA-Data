

import pandas as pd
import os
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup


currentyear = 2020

def make_draft_table(save = True):
	Drafts = pd.DataFrame(  columns=['Year', 'Player', 'Team', 'Ovr', 'College'])
	for year in range(1950, currentyear + 1):# URL page we will scraping (see image above)
		pk = 1
		
		print(year)
		url = "https://www.basketball-reference.com/draft/NBA_{}.html".format(year)	
		html = urlopen(url)
		soup = BeautifulSoup(html)
		g = (soup.find(id = 'stats'))
		table_rows = g.find_all('tr')
		#print('a', table_rows)
		exclude = [['', '', '', '', '', '', ''],[],['Minnesota forfeited the 29th overall pick.']]
		for tr in table_rows:
			#print(tr)
			td = tr.find_all('td')
			#print(type(td))
			#print('a',td)
			row = [i.text for i in td ]
			if(row not in exclude):# and row[0] == 'NBA'):	
				#print(row)	
				dat = [year, row[2], row[1], pk, row[3]]
				newdf = pd.DataFrame(data = [dat],   columns=['Year', 'Player', 'Team', 'Ovr', 'College'])
				Drafts = Drafts.append(newdf)
				pk += 1

	if (save):
		Drafts.to_csv('raw_data/drafts.csv')
	return Drafts
print(make_draft_table())