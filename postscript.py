import numpy as np
import pandas as pd

# loading the npy data eliminates the column names
'''
dataset = np.load('dataset.npy')
colnames = np.load('colnames.npy')
df = pd.DataFrame(dataset,columns=colnames)

bounds = pd.read_csv('bounds.csv', header=None, names=['x1','x2','y1','y2','cx','cy'])
bounds['dist'] = pd.Series(np.sqrt((bounds.cx - bounds.x1)**2 + (bounds.cy - bounds.y1)**2))

# add a column to df to indicate which boundID has closest center to location
temp = []
nrow, ncol = df.shape[0], df.shape[1]
for i in range(nrow):
    tempx = df.loc[i,'x_coordinate']
    tempy = df.loc[i, 'y_coordinate']
    # first see if point lies entirely in a given bounding box, if not then get closest center
    mylist = [(k,np.sqrt((tempx - bounds.loc[k,'cx']) ** 2 + (tempy - bounds.loc[k,'cy']) ** 2)) for k in range(60)
              if bounds.loc[k,'dist'] > np.sqrt((tempx - bounds.loc[k,'cx']) ** 2 + (tempy - bounds.loc[k,'cy']) ** 2)]
    # if the list is not empty, then there is a box that entirely contains point. then update flag to True
    # all IDs where dist from center to edge is bigger than distance from center to current point
    if len(mylist) > 0:
        foundTpl = min(mylist, key=lambda t: t[1]) # found tuple, minimum distance to centers
        temp += [foundTpl[0] + 1] # the index retained
    else:
        # now compute distance to all centers
        fulllist = [(k,np.sqrt((tempx - bounds.loc[k,'cx']) ** 2 + (tempy - bounds.loc[k,'cy']) ** 2)) for k in range(60)]
        foundTpl = min(fulllist, key=lambda t: t[1])
        temp += [foundTpl[0] + 1]
df['boxID'] = pd.Series(temp)
np.save('datasetPost',df)
np.save('colnamesPost', df.columns)
print(df)
'''


df = np.load('datasetPost.npy')
names = np.load('colnamesPost.npy')
df = pd.DataFrame(df,columns=names)
nrow, ncol = df.shape[0], df.shape[1]
boxIDs = df.boxID
### assemble a dictionary that contains list of indices for different boxIDs
dict = {}
for i in range(60):
    dict[i+1] = np.where(boxIDs == i)[0] # with the i+1 we are ok.
#### Imputation
for i in range(nrow):
    cboxId = df.loc[i,'boxID'] # current boxID
    if pd.isnull(df.loc[i, 'census_tract']):
        #print('found', i+1, df.loc[i, 'census_tract'])
        tempx = df.loc[i, 'x_coordinate']
        tempy = df.loc[i,'y_coordinate']
        #mylist = [k for k in range(nrow) if boxIDs[k] == df.loc[i,'boxID'] if k != i] # row indices for observations with same boxID
        mylist = dict[cboxId]
        ind, sdist = 0, np.inf
        for j in mylist:
            if j != i:
                tempx1 = df.loc[j, 'x_coordinate']
                tempy1 = df.loc[j, 'y_coordinate']
                cdist = np.sqrt((tempx - tempx1)**2 + (tempy - tempy1)**2)
                if cdist < sdist and not pd.isnull(df.loc[j,'census_tract']):
                    ind, sdist = j, cdist
        #print(df.loc[ind,'census_tract'])
        df.loc[i,'census_tract'] = df.loc[ind, 'census_tract']

#np.save('datasetImp', df)
#np.save('colnamesPost', df.columns)
#print(df)
#print(any(pd.isnull(df.census_tract)))