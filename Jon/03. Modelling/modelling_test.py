sp# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import seaborn as sns
import dask.dataframe as dd
import pandas as pd

from math import sin, cos, sqrt, atan2, radians
import os
os.getcwd()

# Import Google API file, include encoding='latin1' since not all are utf-8 in the file
google_api = pd.read_csv("Lat Long Canada.csv", encoding='latin1')

google_api.shape

# Check how N/A is imported
google_api['City'][1]
type(google_api['City'][1])

'''
# Import Web Scrape List
web = pd.read_csv("final_school_df_with_address.csv", encoding='latin1')

import re
pattern = re.compile(r'[A-Z]\d[A-Z] *\d[A-Z]\d')

# These have N/A so it returns TypeError instead of AttributeError
# Instead of except AttributeError, we will use Except Error to include the two types of errors
pattern.search(web['Address'][754]).group()

postal=[]

# Replace the items that have do not match the postal code pattern with "None"
for x in range(0, len(web)):
    try:
        postal1 = pattern.search(web['Address'][x]).group()
    except:
        postal1="None"
    postal.append(postal1)
        
len(postal)

postal[:25]    

# Append the new postal code list to the web file
se = pd.Series(postal)

web['Postal Code'] = se.values

web.shape

type(web)

web.to_csv("final_school_df_with_address_postal.csv")
'''
#try mapping postal code first before merging to demostat

#TRY MATCHING POSTAL CODE OF WEB WITH LIST OF GOOGLE API

web = pd.read_csv("final_school_df_with_address_postal.csv", encoding='latin1')

web=web.drop(columns='Unnamed: 0')

len(web)

fsa=[]

for x in range(0, len(web)):
    if web['Postal Code'][x] != "None":
        fsa.append(web['Postal Code'][x][:3])
    else:
        fsa.append(web['Postal Code'][x])
    
se = pd.Series(fsa)
web['FSA']=se.values        
        