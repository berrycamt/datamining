"""
This is the first python file to obtain days and months
"""

import numpy as np
import pandas as pd
import datetime as dt

# this function is useless
def formaldate(string):
	item = string.split("/") # this is the date components
	return dt.date(int(item[2]), int(item[1]), int(item[0])) # so return the date as datetime in the dataframe
# end of useless function
	
# use pd.timestamp() instead. weekday: Mon-Sun: 0-6

df = pd.read_csv('NIJ2016_JAN01_JUL31.csv')
# find out if any dates are missing
df['FormalDate'] = pd.to_datetime(df.occ_date)
df['Weekday'] = pd.Series(map(lambda x: x.weekday(), df.FormalDate)) # Mon-Sun : 0-6

# save
np.save('dataset', df)
colnames = df.columns
np.save('colnames', colnames)
# now this can be grouped and manipulated per variable ...