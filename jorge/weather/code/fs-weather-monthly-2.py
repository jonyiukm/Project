# coding: utf-8

# Exploring Environment Canada Weather Data¶
# This notebook demonstrates how to scrape Environment Canada's weather data using Python with data analysis libraries like pandas and Beautiful Soup.
# 
# 
# For new installations, use !pip install --user as a line of code to install missing packages
# 
# Adapted to extract monthly data and query postal code of weather stations: By J. Lopez
# 
# getMonthlyData function to get the monthly data
# read the download of data from EC
# Conform  geolocation of weather station and province, and find out from coordinates the postal code
# write the data into a csv file including province, stationID and ws name

# In[1]:


def calcPostalC(lat, lng):
## Get the postal code from geoloc
    import geocoder
    g = geocoder.google([lat, lng], method='reverse')
    return g.postal


# In[2]:


def getMonthlyData(stationID, year, month, prov, name):
    print("at ############### getMonthlyData with", year, month, prov, name)
    global val
    
    
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=3".format(stationID, year, month) # 3 is monthly
    URL = base_url + query_url
    time.sleep(2) ## This delay is necessary otherwise the program crashes!! ################################
 
    #TEST
    ## these two lines to avoid the SSL error
    import ssl
    context = context = ssl._create_unverified_context()
    
    ##TEST
    ## read URL
    import urllib2
    station = urllib2.urlopen(URL, context = context)
    station = station.read()
    
    ## read URL
    ##import urllib.request
    ##with urllib.request.urlopen(URL) as response:
    ##    station = response.read()
      
        
    ## Decode
    #sin = station
    #sin = str(sin).encode('utf-8')
    sAll = [s.strip() for s in station.splitlines()]  ## What's doing here??

    # manipulate sAll[3] and sAll[4] to extract geoloc
    
    start = sAll[2].find('latitude/",/"') +13
    end = sAll[2].find('/"')
    lat = sAll[2][start:end]
    
    start = sAll[3].find('longitude/",/"') +14
    end = sAll[3].find('/"')
    lng = sAll[3][start:end]
    
    
    sDet = sAll[19:] ## extract monthly data, data starts at row 19!! ###############
    
    oCols=[
         "Date/Time", ## 23 stats for monthly extract!
         "Year",
         "Month",
         "Mean Max Temp C",
         "Mean Min Temp C", #5
         "Mean Min Temp Flag",
         "Temp Flag",
         "Mean Temp C",
         "Mean Temp Flag",
         "Ext Max Temp", #10
         "Ext Max Temp Flag",
         "Ext Min Temp",
         "Ext Min Temp Flag",
         "Total Rain (mm)",
         "Total Rain Flag", #15
         "Total Snow (mm)", 
         "Total Snow Flag",
         "Total Precip (mm)",
         "Total Precip Flag",
         "Snow Grnd Last Day", #20
         "Snow Grnd Last Day Flag",
         "Dir of Max Gust (10's deg)",
         "Dir of Max Gust Flag",
         "Spd of Max Gust (km/h)",
         "Spd of Max Gust Flag",
          ]
    
    #test OK to split each row by ","
    lst = []
    df = [] ## init df
    
    for i in range(2, len(sDet)): ## from 2..
        new_sDet = str(sDet[i].replace("\"", "")).split(",")    
        lst.append(new_sDet) ## added
        ##print("new_sDet of ", i, "=", new_sDet)
        ##print("len(lst[", i, "][:])=", len(lst[i][:]))
        
        ##print("new_sDet=", new_sDet)
        
    print("len(oCols)=", len(oCols))
    print("len(lst)=", len(lst))
    print("oCols=", oCols[0:len(lst)])
    print("len of oCols[0:len(lst)]=", len(oCols[0:len(lst)]))
    
    print("################ out of for to build lst ######################")
    
    df = pd.DataFrame(lst, columns= oCols[0:len(lst[0])]) ## 25columns converted!! problem is here!! [0:23] added
    
    df['StationID'] = stationID
    df['Province'] = prov
    df['Name'] = name
    df['Latitude']= lat
    df['Longitude']= lng
    
    df['Postal Code']= calcPostalC(lat, lng)
    
    ## Rearrange columns
    
    ## rearranging columns
    df = df[[
             'Province',    #new 1
             'StationID',   #new 2 
             'Name',        #new 3 
             'Latitude',    #new 4
             'Longitude',   #new 5 
             'Postal Code', #new 6
             "Date/Time", 
             "Year",
             "Month",
             "Mean Max Temp C",
             "Mean Min Temp C", #5
             "Mean Min Temp Flag",
             "Temp Flag",
             "Mean Temp C",
             "Mean Temp Flag",
             "Ext Max Temp", #10
             "Ext Max Temp Flag",
             "Ext Min Temp",
             "Ext Min Temp Flag",
             "Total Rain (mm)",
             "Total Rain Flag", #15
             "Total Snow (mm)", 
             "Total Snow Flag",
             "Total Precip (mm)",
             "Total Precip Flag",
             "Snow Grnd Last Day", #20
             "Snow Grnd Last Day Flag",
             "Dir of Max Gust (10's deg)",
             "Dir of Max Gust Flag",
             "Spd of Max Gust (km/h)",
             "Spd of Max Gust Flag",
            ]]

    with open('allSallP.csv', 'a') as f:
        df.to_csv(f, header=val, index = True) ## just for testing changed!!
        print("###### header=", val)
    val = False
    return df


# function that takes in a station ID, the year and month and returns a pandas DataFrame with the downloaded data:

# In[3]:


# include - OK Tested!
def fSoupFrames(province, start_year, max_pages):
    #This is a important piece of code
    ## I need to iterate on the provinces

    # Specify Parameters
    #province = "ON"      # Which province to parse?
    #start_year = "2015"  # I want the results to go back to at least this year or earlier ????
    #max_pages = 10        # Number of maximum pages to parse, EC's limit is 100 rows per page

    for i in range(max_pages):
        startRow = 1 + i*100
        print('Downloading Page: ', i)
    
        base_url = "http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?"
        queryProvince = "searchType=stnProv&timeframe=1&lstProvince={}&optLimit=yearRange&".format(province)
        queryYear = "StartYear={}&EndYear=2017&Year=2017&Month=5&Day=29&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&".format(start_year)
        queryStartRow = "startRow={}".format(startRow)

        response = requests.get(base_url + queryProvince + queryYear + queryStartRow) # Using requests to read the HTML source
        soup = BeautifulSoup(response.text, 'html.parser') # Parse with Beautiful Soup
        soup_frames.append(soup)
    return soup_frames
    


# In[4]:


#sd='Sep2016'
#ed='Sep2017'

def lookUpStation(stationID, sd, ed, prov, name ):
    print("****** at lookUpStation StationID=", stationID, " prov=", prov, "name=", name)
    start_date = datetime.strptime(sd, '%b%Y')
    end_date = datetime.strptime(ed, '%b%Y')

    frames = []
    ## here appends all WS of the province
        
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    
        df = getMonthlyData(stationID, dt.year, dt.month, prov, name) ## what for df then???
        print("################# dt.year=", dt.year, "dt.month=", dt.month)
    return df


# ################################################### main() #############################################################

# In[5]:


import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns ## seaborn: statistical data visualization. Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.
from dateutil import rrule ## he rrule module offers a small, complete, and very fast, implementation of the recurrence rules documented in the iCalendar RFC, including support for caching of results
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from fuzzywuzzy import fuzz ## string matching
import time
import os
import urllib

import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBCStYlYkMxdXJYJjuVEINvU7U8HBarCJ0'

val = True


# In[6]:


# Store each page in a list and parse them later
soup_frames = []
stations_df = [] 


# In[7]:


# need to iterate over all provinces of Canada!
## make a list with all provinces

dProv = {"AL" : "Alberta",
         "BC" : "British Columbia",
         "MB" : "Manitoba",
         "NB" : "New Brunswick",
         "NF" : "New Foundland",
         "NT" : "Nortwest Territories",
         "NS" : "Nova Scotia", 
         "NU" : "Nunavut",
         "ON" : "Ontario",
         "PE" : "Prince Edward Island", 
         "QC" : "Quebec",
         "SK" : "Saskachewan",
         "YT" : "Yukon"}

for key, value in dProv.items():
    print(key)
    soup_frames = fSoupFrames(key, "2015", 10) ## need to supply year!


# Each Weather Station is called a "row", startRow has the number of the starting row in each page, he assumes 100 pages or "rows" per page..
# 
# The soup currently goes nowhere..
# 
# how to determine max_pages?
# 
# This is only the list of stations where to find further information.

# Here loops to each station, gets the stationID, data intervals available for start and end years

# In[8]:


# include
# This cell is being modified to include PROVINCE in the df! 
# another important piece of code

station_data = []

for soup in soup_frames: # For each soup
    forms = soup.findAll("form", {"id" : re.compile('stnRequest*')}) # We find the forms with the stnRequest* ID using regex 
    for form in forms:
        try:
            # The stationID is a child of the form
            station = form.find("input", {"name" : "StationID"})['value']
            
            # The station name is a sibling of the input element named lstProvince
            name = form.find("input", {"name" : "lstProvince"}).find_next_siblings("div")[0].text
            
            prov = form.find("input", {"name" : "Prov"}) ['value'] ## added
            
            # The intervals are listed as children in a 'select' tag named timeframe
            timeframes = form.find("select", {"name" : "timeframe"}).findChildren()
            intervals =[t.text for t in timeframes]
            
            # We can find the min and max year of this station using the first and last child
            years = form.find("select", {"name" : "Year"}).findChildren()            
            min_year = years[0].text
            max_year = years[-1].text
            
            # Store the data in an array
            data = [station, prov, name, intervals, min_year, max_year]
            station_data.append(data)
        except:
            pass

# Create a pandas dataframe using the collected data and give it the appropriate column names
stations_df = pd.DataFrame(station_data, columns=['StationID', 'Province', 'Name', 'Intervals', 'Year Start', 'Year End'])
stations_df.to_csv('stations.csv')
stations_df.head()


# In[9]:


## changeed from hourly to Monthly Data!!
# include
# Show only data with hourly intervals ; Im interested on this as I will be extracting only hourly data!
# 

hourly_stations = stations_df.loc[stations_df['Intervals'].map(lambda x: 'Monthly' in x)]
hourly_stations.to_csv('h_stations.csv') ## saving stations data with hourly data
hourly_stations.head()


# In[10]:


## Here iterate over all monthly stations in all provinces

## not needed allPframes = []
val = True

if os.path.exists("./allSallP.csv"):
    os.remove("./allSallP.csv")
    print("*** allSallP file DELETED ***")
else:
    print("The file does not exist")
        
for index, row in hourly_stations.iterrows():
    print (row["StationID"])
    print (row["Province"])
    print (row["Name"]) 
    ## here is not! print (row['Postal Code'])
    allStations = lookUpStation(row["StationID"], 'Sep2016', 'Sep2017', 
                                row["Province"], row["Name"]) 
    ## What period of information we want?, the longer the period the bigger the data will generate!
    ##nnallPframes.append(allStations) ## aggregating all stations for all provinces!
