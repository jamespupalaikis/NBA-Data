import pandas as pd
import os
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup



#################33####################

heights= pd.read_csv('1979to2020heights.csv')#,index_col = 0)
heights = heights.rename(columns = {'Unnamed: 0': 'PLAYER', '0': 'Height'})



def heightTranslate(hstring):
	a = hstring[0]
	assert(hstring[1] == '-')
	b = hstring[2:]
	return 12*int(a) + int(b)

heights['Height'] = heights['Height'].map(heightTranslate)
heights.to_csv('1979to2020heights.csv')