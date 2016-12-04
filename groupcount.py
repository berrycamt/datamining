import numpy as np
import pandas as pd

df = np.load('datasetImp.npy')
names = np.load('colnamesPost.npy')

df = pd.DataFrame(df, columns=names)
df_box_cat = df.groupby(['boxID', 'CATEGORY']) # this is grouped by boxes and categories
counts = df_box_cat.count() # presents counts per group for all columns
counts_once = df_box_cat['CALL GROUPS'].count() # counts for only one column, thus general # observations per group
#print(df_box_cat.get_group((1,'OTHER'))) # this is enough to find how many observations in total occur in a district
#print(counts_once.loc[1,'BURGLARY'])

counted_df = counts_once.reset_index()
counted_df.columns = ['boxID', 'cat', 'total'] # 1st 4 rows, i.e 0:3 for box 1, next 4 box2 and so on
# this dataframe can allow us to get number of Burglary in a given district by using .loc[row,'cat']
#print(counted_df.loc[0:3,'boxID':'total'])
# use group_by on this data frame to obtain groups of boxID and aggregate on total.
counted_groupB = counted_df.groupby('boxID')
#print(counted_groupB.count()) # group 14 has one missing category
#print(counts_once.loc[14,:]) # this shows that there were no Buglary in district with boxID 14
#print(counted_groupB.aggregate(np.sum))
# we can also group by Category and get total number of Buglary overall for example...
burg =[] # burglary
mvt = [] # motor vehicle theft
other = [] # other
stc = [] # street crime
ind = 0
while ind < (counted_df.shape[0]-3):
    if ind == 52:
        burg += [0]
        mvt += [counted_df.loc[ind, 'total']]
        other += [counted_df.loc[ind + 1, 'total']]
        stc += [counted_df.loc[ind + 2, 'total']]
        ind += 3
    else:
        burg += [counted_df.loc[ind,'total']]
        mvt += [counted_df.loc[ind+1,'total']]
        other += [counted_df.loc[ind+2,'total']]
        stc += [counted_df.loc[ind+3,'total']]
        ind += 4

agg_df = pd.DataFrame({'boxID':list(range(1,61)), 'burg':burg, 'mvt': mvt, 'other':other, 'stc': stc})

# now we wish to add district number and precinct code. we can also merge with the largest dataset
dist_nber = pd.read_csv('distNber.csv', header=None)
dist_nber.columns = ['boxID', 'district']
# precinct based on boxID: 1:20 : NO, 21:40 : CE, 41:60 : EA
precinct = list(map(lambda x: 'NO' if x <= 20 else ('CE' if x <= 40 else 'EA'), range(1,61)))
dist_nber['precinct'] = pd.Series(precinct)
merge_agg = pd.merge(agg_df,dist_nber,on='boxID')

#np.save('boxesdata', merge_agg)
#np.save('boxesdatacols', merge_agg.columns)

#merge_agg.to_csv('boxesdata.csv')