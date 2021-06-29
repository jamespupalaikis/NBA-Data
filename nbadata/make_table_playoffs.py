import pandas as pd
import os
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup

teamDict = {'ATLANTA HAWKS' : 'ATL',
'ST. LOUIS HAWKS' : 'SLH',
'MILWAUKEE HAWKS' : 'MIL',
'TRI-CITIES BLACKHAWKS' : 'TCB',
'BOSTON CELTICS' : 'BOS',
'BROOKLYN NETS' : 'BRK',
'NEW JERSEY NETS' : 'NJN',
'CHICAGO BULLS' : 'CHI',
'CHARLOTTE HORNETS' : 'CHH', ###chh til 2004, then cho
#CHARLOTTE HORNETS : CHO,
'CHARLOTTE BOBCATS' : 'CHA',
'CLEVELAND CAVALIERS' : 'CLE',
'DALLAS MAVERICKS' : 'DAL',
'DENVER NUGGETS' : 'DEN',
'DETROIT PISTONS' : 'DET',
'FORT WAYNE PISTONS' : 'FWP',
'GOLDEN STATE WARRIORS' : 'GSW',
'SAN FRANCISCO WARRIORS' : 'SFW',
'PHILADELPHIA WARRIORS' : 'PHI',
'HOUSTON ROCKETS' : 'HOU',
'INDIANA PACERS' : 'IND',
'LOS ANGELES CLIPPERS' : 'LAC',
'SAN DIEGO CLIPPERS' : 'SDC',
'BUFFALO BRAVES' : 'BUF',
'LOS ANGELES LAKERS' : 'LAL',
'MINNEAPOLIS LAKERS' : 'MIN',
'MEMPHIS GRIZZLIES' : 'MEM',
'VANCOUVER GRIZZLIES' : 'VAN',
'MIAMI HEAT' : 'MIA',
'MILWAUKEE BUCKS' : 'MIL',
'MINNESOTA TIMBERWOLVES' : 'MIN',
'NEW ORLEANS PELICANS' : 'NOP',
'NEW ORLEANS/OKLAHOMA CITY HORNETS' : "NOK",
'NEW ORLEANS HORNETS' : 'NOH',
'NEW YORK KNICKS' : 'NYK',
'OKLAHOMA CITY THUNDER' : 'OKC',
'SEATTLE SUPERSONICS' : 'SEA',
'ORLANDO MAGIC' : 'ORL',
'PHILADELPHIA 76ERS' : 'PHI',
'SYRACUSE NATIONALS' : 'SYR',
'PHOENIX SUNS' : 'PHO',
'PORTLAND TRAIL BLAZERS' : 'POR',
'SACRAMENTO KINGS' : 'SAC',
'KANSAS CITY KINGS' : 'KCK',
'KANSAS CITY-OMAHA KINGS' : 'KCK',
'CINCINNATI ROYALS' : 'CIN',
'ROCHESTER ROYALS' : 'ROR',
'SAN ANTONIO SPURS' : 'SAS',
'TORONTO RAPTORS' : 'TOR',
'UTAH JAZZ' : 'UTA',
'NEW ORLEANS JAZZ' : 'NOJ',
'WASHINGTON WIZARDS' : 'WAS',
'WASHINGTON BULLETS' : 'WAS',
'CAPITAL BULLETS' : 'CAP',
'BALTIMORE BULLETS' : 'BAL',
'CHICAGO ZEPHYRS' : 'CHI',
'CHICAGO PACKERS' : 'CHI',
'ANDERSON PACKERS' : 'AND',
'CHICAGO STAGS' : 'CHI',
'INDIANAPOLIS OLYMPIANS' : 'IND',
'SHEBOYGAN REDSKINS' : 'SRS',
'ST. LOUIS BOMBERS' : 'SLB',
'WASHINGTON CAPITOLS' : 'WAS',
'WATERLOO HAWKS' : 'WAT',
'SAN DIEGO ROCKETS': 'SDR'}


def build_base():
	url = 'https://www.basketball-reference.com/playoffs/'
	html = urlopen(url)
	soup = BeautifulSoup(html)
	g = (soup.find(id = 'champions_index'))
	table_rows = g.find_all('tr')
	games = []

	j = 2020
	for tr in table_rows:
		td = tr.find_all('td')
		row = [i.text for i in td]
		    #print(row)
		if(len(row) > 0):
			if(row[0] == 'NBA'):
			    games.append([j] + row[1:3])
			    j -= 1

	df = pd.DataFrame(games)
	df = df.rename(columns = {0: 'Year', 1 : 'Winner', 2: 'RunnerUp' })
	df['Winner']  = df['Winner'].map(lambda x: teamDict[x.upper()])
	df['RunnerUp']  = df['RunnerUp'].map(lambda x: teamDict[x.upper()])
	df['Rest'] = df['Year']
	df['FMVP'] = df['Year']
	#print(df)
	return df



def make_playoffs_table( save = True):
	start, stop = 1950, 2020
	base = build_base()
	for year in range(start, stop + 1):
		print(year)
		url = 'https://www.basketball-reference.com/playoffs/NBA_{}.html'.format(year)
		html = urlopen(url)
		soup = BeautifulSoup(html, features="lxml")
		g = (soup.find(id = 'team-stats-per_game'))
		table = soup.find('table')
		#print(table)
		table_rows = g.find_all('tr')
		games = []
		i = 0
		for tr in table_rows:
			if(i != 0):
			    td = tr.find_all('td')
			    row = [i.text for i in td]
			    games.append(row[:2])
			i += 1
		num = len(games) - 1
		winstr = soup.find_all('p', limit  = 5)
		rest = [teamDict[games[i][0].upper()] for i in range(num)]
		#print(base)
		currentYear = base.loc[base['Year'] == year]
		rest.remove(currentYear['Winner'].values[0])
		rest.remove(currentYear['RunnerUp'].values[0])
		rest_teams = ''
		for team in rest:
			rest_teams += team
			rest_teams += ' '
		FMVP = 'N/A'
		if(year >= 1969):
			FMVP = winstr[3].text[12:winstr[3].text.find('(') - 1]
		
		base= base.replace({'FMVP': {year: FMVP}})
		base= base.replace({'Rest': {year: rest_teams}})
		base = base.loc[(base['Year'] >= start) & (base['Year'] <= stop) ]
	if (save):
		base.to_csv('raw_data/%ito%iplayoffs.csv' %(start, stop))
	return base

make_playoffs_table()