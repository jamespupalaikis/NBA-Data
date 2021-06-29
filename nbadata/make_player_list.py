import pandas as pd 
import numpy as np 

statstable = pd.read_csv('rawdata/1950to2020stats.csv')


print(statstable.head())
playerlist = []
def makeplayerlist(name, list = playerlist):
	if (name in list):
		return False
	else:
		list.append(name)
		return True

statstable['Player'].map(makeplayerlist)

print(len(playerlist))

print(playerlist[3000])

(pd.DataFrame(np.array(playerlist))).to_csv('rawdata/playerlist.csv')
