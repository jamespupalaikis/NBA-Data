import pandas as pd
import numpy as np

##########Yearly stats
seasons = pd.read_csv('nbadata/rawdata/1950to2020stats.csv')
playoffs = pd.read_csv('nbadata/rawdata/1950to2020playoffs.csv')
awards =  pd.read_csv('nbadata/rawdata/1950to2020accolades.csv')
allnba  = pd.read_csv('nbadata/rawdata/allnba.csv')
alldef = pd.read_csv('nbadata/rawdata/alldef.csv')

#############################now to put them together
seasons = seasons.drop('Unnamed: 0', axis = 1)
seasons['MVP'] = 0
seasons['DPOY'] = 0
seasons['AllNBA'] = 0
seasons['AllDef'] = 0
seasons['Playoffs'] = 0
seasons['FMVP'] = 0

#First year of MVP: 1956
#first year of dpoy: 1983
MVPs = awards['MVP'].to_list()
MVPs = filter(lambda x: type(x) == type('x'),MVPs)
MVPs = [x for x in MVPs]
MVPs.reverse()

for i in range(1956, 2021,):
    mvp = MVPs.pop()
    playerseason = seasons.loc[seasons['Year']==i].loc[seasons['Player']== mvp]
    a = (playerseason.index)
    seasons._set_value(a,'MVP', 1)

DPOYs= awards['DPOY'].to_list()
DPOYs = filter(lambda x: type(x) == type('x'),DPOYs)
DPOYs = [x for x in DPOYs]
DPOYs.reverse()

for i in range(1983, 2021,):
    dpoy = DPOYs.pop()
    playerseason = seasons.loc[seasons['Year']==i].loc[seasons['Player']== dpoy]
    a = (playerseason.index)
    seasons._set_value(a,'DPOY', 1)
##############Now for All NBA
##############################
#TODO: Fix players getting last names cut off in older years
##############################
#transform years
allnba['Year'] = allnba['Year'].apply(lambda x:  x[0:2] + x[5:7])
alldef['Year'] = alldef['Year'].apply(lambda x:  x[0:2] + x[5:7])

allnba = allnba.loc[allnba['League'] == 'NBA']
alldef = alldef.loc[alldef['League'] == 'NBA']

#Transform AllNBA##################
years = allnba['Year'].to_list()
players = allnba['Player'].to_list()
team = allnba['Team'].to_list()

while(years != []):
    yr = years.pop()
    plyr = players.pop()
    tm = team.pop()

    playerseason = seasons.loc[seasons['Year'] == int(yr)].loc[seasons['Player'] == plyr]
    a = (playerseason.index)
    seasons._set_value(a, 'AllNBA', tm)


#Transform AllDef Teams

years = alldef['Year'].to_list()
players = alldef['Player'].to_list()
team = alldef['Team'].to_list()

while(years != []):
    yr = years.pop()
    plyr = players.pop()
    tm = team.pop()

    playerseason = seasons.loc[seasons['Year'] == int(yr)].loc[seasons['Player'] == plyr]
    a = (playerseason.index)
    seasons._set_value(a, 'AllDef', tm)



##############SETUP PLAYOFFS COLUMN

#print(v.index)

years = playoffs['Year'].to_list()
win = playoffs['Winner'].to_list()
ru = playoffs['RunnerUp'].to_list()
rest = playoffs['Rest'].to_list()
FMVP = playoffs['FMVP'].to_list()
#team = playoffs['Team']

#######The Playoff structure is as follows:
#Current: 1st place: winner, 2nd place, runnerup, 3rd tie: 1st 2 rest, 4th tie: Next 4 rest, 5th Tie: next 8 rest
#oh god its so complicated im just gonna use 1 as a win 2 as a runner up and forget the rest
#edit 3 will now denote 'made the playoffs'

while(years != []):
    yr = years.pop()
    w = win.pop()
    r = ru.pop()
    rs = rest.pop()
    fm = FMVP.pop()

    playerz = seasons.loc[seasons['Year'] == int(yr)].loc[seasons['Tm'] == w]
    a = (playerz.index)
    for i in a:
        seasons._set_value(i, 'Playoffs', 1)

    playerz = seasons.loc[seasons['Year'] == int(yr)].loc[seasons['Tm'] == r]
    a = (playerz.index)
    for i in a:
        seasons._set_value(i, 'Playoffs', 2)

    playerz = seasons.loc[seasons['Year'] == int(yr)].loc[seasons['Player'] == fm]
    a = (playerz.index)
    seasons._set_value(a, 'FMVP', 1)

    for j in rs.split():
        playerz = seasons.loc[seasons['Year'] == int(yr)].loc[seasons['Tm'] == j]
        a = (playerz.index)
        for i in a:
            seasons._set_value(i, 'Playoffs', 3)

#v = (seasons.loc[seasons['Player'] == "Shaquille O'Neal"])
#print(v)


#Now to construct the per-player table of career stats

players = pd.read_csv('nbadata/rawdata/playerlist.csv').drop('Unnamed: 0', axis = 1)
draft = pd.read_csv('nbadata/rawdata/drafts.csv').drop('Unnamed: 0', axis = 1)
height =pd.read_csv('nbadata/rawdata/1979to2020heights_.csv').drop('Unnamed: 0', axis = 1)
HOF = pd.read_csv('nbadata/rawdata/HOFList.csv')

#print(player)
####Feed in college and draft info
players['Drafted'] = 0#
players['DraftedBy'] = 'N/A'#
players['FirstTeam'] = 'N/A'
players['DraftYear'] = 0#
players['College'] = 0#
players['Height'] = 0#
players['HOF'] = 0#

year = draft['Year'].to_list()
playr = draft['Player'].to_list()
college = draft['College'].to_list()
pick = draft['Ovr'].to_list()
team = draft['Team'].to_list()

while(year != []):
    #print(year)
    yr = year.pop()#
    plyr = playr.pop()#
    clg = college.pop()#
    ovr = pick.pop()#
    tm = team.pop()#
    playerind = players.loc[players['0'] == plyr]
    pi =playerind.index
    players._set_value(pi, 'DraftYear', yr)
    players._set_value(pi, 'Drafted', ovr)
    players._set_value(pi, 'DraftedBy', tm)
    players._set_value(pi, 'College', clg)

###Feed in height

howhigh = height['Height'].to_list()
playr = height['Player'].to_list()
while(playr != []):
    plyr = playr.pop()
    ht = howhigh.pop()
    playerind = players.loc[players['0'] == plyr]
    pi = playerind.index
    players._set_value(pi, 'Height', ht)

###and HOF status...

playr = HOF['Player'].to_list()
for guy in playr:
    playerind = players.loc[players['0'] == guy]
    pi = playerind.index
    players._set_value(pi, 'HOF', 1)
print(players.loc[players['College'] == 'Duke'])


players.to_csv('playerdata.csv')
seasons.to_csv('seasondata.csv')