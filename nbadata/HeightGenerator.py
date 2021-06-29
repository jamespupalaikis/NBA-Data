from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from sklearn import decomposition
import numpy as np
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc
# NBA season we will be analyzing
year = 2020# URL page we will scraping (see image above)
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)# this is the HTML from the given URL

html = urlopen(url)
soup = BeautifulSoup(html)

####
# use findALL() to get the column headers
soup.findAll('tr', limit=2)# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]
#print(headers)

# avoid the first header row
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

stats = pd.DataFrame(player_stats, columns = headers)
'''

#stats['team']

#print(headers)
#['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

#stats['Tm'] = pd.Categorical(stats['Tm'])
#stats['Pos'] = pd.Categorical(stats['Pos'])
def flatten_lists(the_lists):
    result = []
    for _list in the_lists:
        result += _list
    return result

def removeStar(aString):
		if ((aString[len(aString)-1:len(aString)]) == '*'):
			#print(len(aString) - 1)
			return aString[0:len(aString) - 1]
		else:
			return aString



def getPlayers(start,end):
	total = []

	for year in range(start, end+1):
		url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)# this is the HTML from the given URL
		html = urlopen(url)
		soup = BeautifulSoup(html, features = 'lxml')	# use findALL() to get the column headers
		soup.findAll('tr', limit=2)# use getText()to extract the text we need into a list
		headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
		headers = headers[1:]
		rows = soup.findAll('tr')[1:]
		player_stats = [[td.getText() for td in rows[i].findAll('td')]
		            for i in range(len(rows))]

		stats = pd.DataFrame(player_stats, columns = headers)
	################3###
		
		names = stats.pop('Player')

		total += (names.tolist())
	strip = np.array(total)
	print(type(strip))
	
	strip = np.unique(strip[strip != None])

	

	a = np.array([removeStar(name) for name in strip])
	return a



a = getPlayers(2011, 2014)

print(len(a))
'''
def heightTranslate(hstring):
	a = hstring[0]
	assert(hstring[1] == '-')
	b = hstring[2:]
	return 12*int(a) + int(b)



teamNames = np.array(['ATL','SLH','MIL','TCB','BOS','BRK','NJN','CHI','CHH','CHO','CHA','CLE','DAL','DEN','DET','FWP','GSW',
'SFW','HOU','IND','LAC','SDC','BUF','LAL','MIN','MEM','VAN','MIA','MIL','NOP','NOK','NOH','NYK','OKC','SEA',
'ORL','PHI','SYR','PHO','POR','SAC','KCK','CIN','ROR','SAS','TOR','UTA','NOJ','WAS','CAP','BAL','AND'])


def heightDict(start, end):
	heights = {}
	for year in range(start, end + 1): 
		print('parsing ' + str(year))
		for team in teamNames:
			roster = get_roster(team, year)
			#print(roster
			#print(roster == None)
			if(type(roster) == type(None)):
				continue
			#parsed = roster.loc[(roster['PLAYER']) not in  heights]
			names = roster['PLAYER'].tolist()
			hvals = roster['HEIGHT'].tolist()
			while(names != []):
				n = names.pop()
				m = hvals.pop()
				if (n not in heights):
					heights[n] = m
	return heights
start = 1979
end = 2020
h = heightDict(start,end)
#print(h['LeBron James'])
df = pd.DataFrame.from_dict(h, columns = [ 'Height'], orient="index")
#df.rename(columns={"0": "Height", "": "Player"})
#print(df)
df['Height'] = df['Height'].map(heightTranslate)#RENAME COLUMNS TO "PLAYER", "HEIGHT"


def fix(name):
	if(name[-1] == ')'):
		return name[:-5]
	else:
		return name

#df['PLAYER'] = df['PLAYER'].apply(fix)
df.to_csv('%ito%iheights_.csv' %(start, end))
#print(stats.head(5))
back = pd.read_csv('%ito%iheights_.csv' %(start, end))
back = back.rename(columns = {'Unnamed: 0': 'Player'})
back.to_csv('%ito%iheights_.csv' %(start, end))
#print(back.columns)
#pca = decomposition.PCA(n_components = 3)
#cut = stats[[ 'STL', 'BLK', 'TOV', 'PF', 'PTS']]
#pca.fit(cut.applymap(lambda x: float(x) if (type(x) == type('s')) and x != '') else 0))
