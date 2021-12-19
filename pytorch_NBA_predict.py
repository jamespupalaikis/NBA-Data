import pandas as pd
import numpy as np


#want to compile x data with the following:
#[height, rookie ppg, rookie 3p%, rookie mp, rookie 2p%, rookie drb, rookie orb, rookie assists, rookie TO, rookie steals]...

#experiment with different labels, possibilities include whther they made all-nba, mvp, etc...

all = pd.read_csv('nbadata/rawdata/allnba.csv').drop(columns = ['Unnamed: 0'])
alldef = pd.read_csv('nbadata/rawdata/alldef.csv').drop(columns = ['Unnamed: 0'])
both = all['Player'].append(alldef['Player'])



height = pd.read_csv('nbadata/rawdata/1979to2020heights_.csv').drop(columns = ['Unnamed: 0'])
allstats = pd.read_csv('nbadata/rawdata/1950to2020stats.csv').drop(columns = ['Unnamed: 0'])
stats = allstats.loc[allstats['Year'] > 1968].drop_duplicates(subset = 'Player').loc[allstats['Year'] > 1980]

print(stats.columns)


#gonna use the statsdataframe as a base because it will be mostly subtractive.
stats = stats[stats['Player'].isin(height['Player'].to_list())]
#merge the height column
stats = stats.merge(height, left_on = 'Player', right_on = 'Player')


hsave = stats['Height']#save this for later
stats = stats.drop(columns = ['Height'])
hsave = (hsave - hsave.mean())/hsave.std()


#keep the names
names = stats['Player']
namescopy = names.to_list()
#drop non-numerocal stats
stats = stats.drop(columns = ['Player', 'Pos', 'Tm' ])


#normalize on a per-year basis, not jus tto rookies but including all players (from allstats df)
start = stats.loc[stats['Year'] == 1980]
yeargrab = allstats.loc[allstats['Year'] == 1980]
startnorm = (start-yeargrab.mean())/yeargrab.std()
startnorm['Year'] = 0.0
for i in range(1981,2021):
    year = stats.loc[stats['Year'] == i]
    yeargrab = allstats.loc[allstats['Year'] == i]
    yearnorm = (year - yeargrab.mean()) / yeargrab.std()
    yearnorm['Year'] = (i - 1980)/(2020-1981)
    startnorm = startnorm.append(yearnorm, ignore_index = True, sort = False)

startnorm['Height'] = hsave

############
#now to stick the labels on:
x_vals = startnorm.to_numpy().tolist()

#print(startnorm['Year'])


def create_labels(data, names, checklist):
    running  = []
    x = []
    y = []
    while(data != []):
        name = names.pop()
        xval = data.pop()
        x.append(xval)
        if (name in checklist.to_list()):
            #print(name)
            #running.append(np.array((xval, 1)))
            y.append(1.)
        else:
            #running.append(np.array((xval, 0)))
            y.append(0.)
    assert(names == [])
    return  np.array(x), np.array(y)

x,y= create_labels(x_vals, namescopy, both)

import random


c = list(zip(x, y))

random.shuffle(c)

x, y = zip(*c)


val_split = 0.1
datalen = len(x)
train_x = x[:int((1-val_split)* datalen)]
train_y = y[:int((1-val_split)* datalen)]

test_x = x[int((1-val_split)* datalen):]
test_y = y[int((1-val_split)* datalen):]
'''
train_data = data[:int((1-val_split)* datalen)]
test_data = data[int((1-val_split)* datalen):]'''


##########################################################################
#Data sorted, now to run through a NN
#########################################################################

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose

import matplotlib.pyplot as plt

##########################################


#train_data = np.array(train_data)
#test_data = np.array(test_data)

batch_size = 32
learn = 0.0001
epochs = 10
##########################################



class customData(Dataset):
    def __init__(self,x,y):
        self.X = torch.FloatTensor(x)
        self.y = torch.FloatTensor(y)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        xdat = self.X[index]
        ydat = self.y[index]
        return (xdat, ydat)


#train_x = train_x.astype(np.float32)
#train_y = train_y.astype(np.long)
#test_x = test_x.astype(np.float32)
#test_y = test_y.astype(np.long)

transformed_train = customData(train_x, train_y)
transformed_test = customData(test_x, test_y)



train_dataloader = DataLoader(transformed_train, batch_size=batch_size)
test_dataloader = DataLoader(transformed_test, batch_size=batch_size)

'''for X, y in train_dataloader:
    print("Shape of X [N, C, H, W]: ", X.shape)
    print("Shape of y: ", y.shape, y.dtype)
    break'''

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28, 64),
            nn.ReLU(),
            nn.Linear(64,128),
            nn.ReLU(),
            nn.Linear(128,1)
        )

    def forward(self,x):
        #print(x)
        #x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = Network().to(device)
print(model)

#loss_fn = nn.CrossEntropyLoss()
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learn)






def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (x,y) in enumerate(dataloader):
        x,y = x.to(device), y.to(device)

        #compute error
        pred = model(x)
        loss = loss_fn(pred, y)

        #backpropogate
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if(batch % 100 == 0):
            loss, current = loss.item(), batch * len(x)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

#validate against the test dataset as well
def test(dataloader, model, loss_fn):
    size =  len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0,0
    with torch.no_grad():
        for x,y in dataloader:
            x,y = x.to(device), y.to(device)

            pred = model(x)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
    return (correct, test_loss)

runstats = []
for t in range(epochs):
    print('epoch ' , t + 1, ' out of ', epochs)
    train(train_dataloader, model, loss_fn, optimizer)
    (acc, loss) = test(test_dataloader, model, loss_fn)
    runstats.append((acc,loss))
'''
plt.subplot(2,1,1)
plt.plot([a[0] for a in stats])
plt.title(label = 'accuracy')

plt.subplot(2,1,2)
plt.plot([a[1] for a in stats])
plt.title(label = 'loss')
plt.show()
'''
