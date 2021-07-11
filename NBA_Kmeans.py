import pandas as pd




#players = pd.read_csv('nbadata/playerdata.csv')
seasons = pd.read_csv('nbadata/seasondata.csv')

seasons = seasons.loc[seasons['Year'] >= 1980]#make the cutoff at 1980 for better data
print(seasons.columns)
players = pd.unique(seasons['Player'])#list of players for our dataset
print(seasons.columns)
#Now to create a DF of the average stats from the player's 5 consecutive seasons with the most games started (chosen somewhat arbitrarily, I was going to use the 5 best PER seasons, but I do not have that data)
data = pd.DataFrame(players,columns = ['Player'])
data['Yr'] = 0 #first year of 5yr average
data['GS'] = 0
data['MP'] = 0
data['3P'] = 0
data['3P%'] = 0
data['2P'] = 0
data['2P%'] = 0
data['FTA'] = 0
data['FT%'] = 0
data['ORB'] = 0
data['DRB'] = 0
data['AST'] = 0
data['STL'] = 0
data['BLK'] = 0
data['TOV'] = 0
data['PTS'] = 0
for guy in players:
    print(guy)
    stats = seasons.loc[seasons['Player'] == guy]
    runs = stats.count()['Player'] - 4
    startage = stats['Age'].to_list()[0]
    firstyr = stats['Year'].to_list()[0]
    if(runs < 0):
        av = stats.mean()
        y = firstyr
    else:
        max = [startage,0]
        for i in range(runs):
            check = stats.loc[stats['Age'] >= startage + i].loc[stats['Age'] < startage + i + 5].sum()
            if(check['GS'] > max[1]):
                max[0] = startage + i
                max[1] = check['GS']
                y = firstyr + i
        av = stats.loc[stats['Age'] >= max[0]].loc[stats['Age'] < max[0] + 5].mean()
    playerind = data.loc[data['Player'] == guy]
    pi = playerind.index
    data._set_value(pi, 'Yr', y)
    for col in data.columns[2:]:
        data._set_value(pi, col, av[col])

data= data.dropna()
print(data)
data.to_csv('best5yraverage.csv')


import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

data = data.drop(columns= ['Player', 'Yr'])
data = data.to_numpy()

print(data)
scaler = StandardScaler()
sdata = scaler.fit_transform(data)
kmeans = KMeans(init="random",n_clusters=3,n_init=10,max_iter=300,random_state=42)
kmeans.fit(sdata)

print(kmeans.n_iter_)