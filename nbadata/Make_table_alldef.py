#'https://www.basketball-reference.com/awards/all_defense.html''



import pandas as pd
import os
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup

def make_alldef_table(save = True):

	url = 'https://www.basketball-reference.com/awards/all_defense.html'
	html = urlopen(url)
	soup = BeautifulSoup(html)
	g = (soup.find(id = 'awards_all_defense'))

	#establish a table of years because they are in headers, not cells
	years =[] 
	headers= g.find_all('th')
	headexclude = [' ', '','  ', 'Season', 'Lg', 'Tm' ]
	for th in headers:
		if(th.text not in headexclude):
			#print('a', th.text, len(th.text))
			years.append(th.text)

	years = years[5:]
	years.reverse()

	AllDef = pd.DataFrame(  columns=['Year', 'Player', 'Team', 'League'])
	#print(g)
	table_rows = g.find_all('tr')
	exclude = [['', '', '', '', '', '', ''],[]]
	for tr in table_rows:
		#print(tr)
		td = tr.find_all('td')
		#print(type(td))
		#print('a',td)
		row = [i.text for i in td ]
		if(row not in exclude):# and row[0] == 'NBA'):		
			#print('b',row)
			year = years.pop()
			team = int(row[1][0])
			for i in row[2:]:
				dat = [[year,i[:],team,row[0] ]]
				newdf = pd.DataFrame( data = dat, columns=['Year', 'Player', 'Team', 'League'])
				#print(newdf)
				AllDef = AllDef.append(newdf)

		
	

			#mvps.append(row[1:2])

	
	print(AllDef)
	#mvps = list(filter(lambda x: (x != []), mvps))
	#mvps += [['N/A'] for i in range(6)]


	#mvplist = pd.DataFrame(mvps[::-1])

	#mvplist['Year'] = range(1950,2021)
	#mvplist = mvplist.rename(columns = {0 : 'MVP'})
	if (save):
		AllDef.to_csv('raw_data/alldef.csv')
	return AllDef

make_alldef_table()
