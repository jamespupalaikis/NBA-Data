from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from sklearn import decomposition
import numpy as np
import matplotlib.pyplot as plt
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc



heights= pd.read_csv('rawdata/1979to2020heights_.csv')#,index_col = 0)
heights = heights.rename(columns = {'Unnamed: 0': 'PLAYER', '0': 'Height'})

'''

def heightTranslate(hstring):
	a = hstring[0]
	assert(hstring[1] == '-')
	b = hstring[2:]
	return 12*int(a) + int(b)
print(heights)
heights['Height'] = heights['Height'].map(heightTranslate)
print(heights)'''

#heights['HGROUP'] = heights['HEIGHT'].map(groupplayers) #create new column val for height group

def hofFilter(name): #trim off the '*' from the names of HOF players for mapping
	if (name == None):
		return None
	if(name[-1] == '*'):
		return name[:-1]
	else: 
		return name

def helpFloat(line): #float() function, but replaces ' ' with 0 
	if(type(line) == type(None)):
		return None
	#	return 696969
	if (line == ' ' or line == ''):
		return 0.0
	else:
		return  float(line)





seasons = pd.DataFrame([])

def compile(start, end, base, h = True):#returns player time data list for each height group in order
	yearSeries = range(start, end + 1)

	for year in range(start, end + 1):# URL page we will scraping (see image above)
	#['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
		print(year)
###########
##Add aggregating nparray and iterate over years, convert height to inches, cmon
###########

		url = "https://www.basketball-reference.com/leagues/NBA_{}_totals.html".format(year)# this is the HTML from the given URL
		html = urlopen(url)
		soup = BeautifulSoup(html)
		soup.findAll('tr', limit=2)# use getText()to extract the text we need into a list
		headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
		headers = headers[1:]
		rows = soup.findAll('tr')[1:]
		player_stats = [[td.getText() for td in rows[i].findAll('td')]
		            for i in range(len(rows))]
		stats = pd.DataFrame(player_stats, columns = headers)
		#heights['HOF'] = False
		stats['Player'] = stats['Player'].map(hofFilter)
		stats = stats.drop_duplicates(subset = 'Player', keep='last')

		stats[['Age',  'G', 'GS', 'MP', 'FG', 'FGA',
		 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
		 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']]\
		 = stats[['Age',  'G', 'GS', 'MP', 'FG', 'FGA',
		 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
		 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']].applymap(helpFloat)

		#print(stats.dtypes)
		if(h == True):
			statGroup = stats.merge(heights, left_on = 'Player', right_on = 'PLAYER' )
			statGroup.pop('PLAYER')
			stats = statGroup
		stats['Year'] = year
		base = pd.concat([base, stats])

		#print(stats)
	return base.dropna()

def make_stats_table(start, stop, heights = True, save = True):

	a = compile(start,stop,seasons, h = False)
	#print(a)
	if(save):
		if(heights):
			a.to_csv('%ito%istatswithheight.csv' %(start, stop))
		else:

			a.to_csv('%ito%save.csv' %(start, stop))
	return a




a = make_stats_table(1950, 2020, False, True)


print(a)






