# coding: utf-8

# Exploring Environment Canada Weather Data
# 
# This notebook demonstrates how to scrape Environment Canada's weather data using Python with data analysis libraries like pandas and Beautiful Soup.
# 
# Here import all necessary libraries
# 
# For new installations, use !pip install --user as a line of code to install missing packages
# 
# Adapted to extract Ontario and Toronto data: By J. Lopez
# 
# getMonthlyData function to get the monthly data
# read the download of data from EC
# Conform  geolocation of weather station and province, and find out from coordinates the postal code
# write the data into a csv file including province, stationID and ws name
# 
# This version extracts the latest monthly available data per weather station, per province
# 
# This version corrects querying google for the postal code everytime the weather station changes.
# 
# This version only considers weather stations in Ontario.
# 
# This version get data by the hour the volume of data produced is huge:
# 
# 30days per month x 24 hours a day x 12 months = 8642 records per station!
# 

# In[1]:


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
import urllib2
import arrow ## to get today's date

import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBCStYlYkMxdXJYJjuVEINvU7U8HBarCJ0'

import geocoder

val = True
postal = "XXX XXX"

first_time = True

import ssl
context = context = ssl._create_unverified_context()

p = 0


# In[2]:


def calcPostalC(lat, lng, flagPC):
## Get the postal code from geoloc
    #import geocoder
    global p, postal
    print("## at calcPostalC, flagPC =", flagPC)
    if flagPC:
        g = geocoder.google([lat, lng], method='reverse')
        p+=1
        print("## at calcPostal #queries to google:", p)
        postal = g.postal
    
    return postal


# In[3]:


def getHourlyData(stationID, year, month, prov, name, flagPC):
    print("at ############### getMonthlyData with", year, month, prov, name, flagPC)
    global val
    
    
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month) # 1 is hourly
    URL = base_url + query_url
    time.sleep(2) ## This delay is necessary otherwise the program crashes!! ################################
 
    #TEST
    ## these two lines to avoid the SSL error
    #import ssl
    #context = context = ssl._create_unverified_context()
    
    ##TEST
    ## read URL
    #import urllib2
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
    
    
    sDet = sAll[17:] ## extract monthly data, data starts at row 17!! ###############
    
    oCols=[
        "Date/Time",
        "Year",
        "Month",
        "Day",
        "Time", #5
        "Temp (°C)",
        "Temp Flag",
        "Dew Point Temp (°C)",
        "Dew Point Temp Flag",
        "Rel Hum (%)", #10
        "Rel Hum Flag",
        "Wind Dir (10s deg)",
        "Wind Dir Flag",
        "Wind Spd (km/h)",
        "Wind Spd Flag", #15
        "Visibility (km)",
        "Visibility Flag",
        "Stn Press (kPa)",
        "Stn Press Flag",
        "Hmdx", #20
        "Hmdx Flag",
        "Wind Chill",
        "Wind Chill Flag",
        "Weather"
          ]
    
    #test OK to split each row by ","
    lst = []
    df = [] ## init df
    
    for i in range(2, len(sDet)): ## from 2..
        new_sDet = str(sDet[i].replace("\"", "")).split(",")    
        lst.append(new_sDet) ## added

    
    #print("################ out of for to build lst ######################")
    try:
        df = pd.DataFrame(lst, columns= oCols) ## 24 columns converted!!   
    
        ## Filterout by year
    
        ## before df = df[df['Year'] >= year] 
        df = df[df['Year'] >= df['Year'].max()]
        ##################################

        df['StationID'] = stationID
        df['Province'] = prov
        df['Name'] = name
        df['Latitude']= lat
        df['Longitude']= lng

        df['Postal Code']= calcPostalC(lat, lng, flagPC)

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
                    "Day",
                    "Time", #5
                    "Temp (°C)",
                    "Temp Flag",
                    "Dew Point Temp (°C)",
                    "Dew Point Temp Flag",
                    "Rel Hum (%)", #10
                    "Rel Hum Flag",
                    "Wind Dir (10s deg)",
                    "Wind Dir Flag",
                    "Wind Spd (km/h)",
                    "Wind Spd Flag", #15
                    "Visibility (km)",
                    "Visibility Flag",
                    "Stn Press (kPa)",
                    "Stn Press Flag",
                    "Hmdx", #20
                    "Hmdx Flag",
                    "Wind Chill",
                    "Wind Chill Flag",
                    "Weather"
                ]]

        with open('fHourlyEC.csv', 'a') as f:
            df.to_csv(f, header=val, index = False) ## just for testing changed!!
            print("###### header=", val)
        val = False
        flagPC = False; print("at getMontlhyData flagPC=", flagPC)
    except:
        print("++++++++++++++ ERROR in converting data into dataframe ++++++++++++++++++++")
        pass
            
    return df, flagPC


# function that takes in a station ID, the year and month and returns a pandas DataFrame with the downloaded data:

# In[4]:


def fSoupFrames(province, start_year, max_pages):
    d=arrow.now().format('YYYY-MM-DD')
    print("## at FSoupFrames:", start_year, d[0:4], d[0:4], d[5:7], d[8:10])
    
    for i in range(max_pages):
        startRow = 1 + i*100
        print('Downloading Page: ', i)
    
        base_url = "http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?"
        queryProvince = "searchType=stnProv&timeframe=1&lstProvince={}&optLimit=yearRange&".format(province)
        queryYear = "StartYear={}&EndYear={}&Year={}&Month={}&Day={}&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=&txtCentralLongSec=0&".format(start_year, d[0:4], d[0:4], d[5:7], d[8:10])
        queryStartRow = "startRow={}".format(startRow)

        # http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?
        #        searchType=stnProv&timeframe=1&lstProvince=NU&optLimit=yearRange&
        #        StartYear={}&EndYear={}&Year={}&Month={}&Day={}
        #        &selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0
        #        &txtCentralLongSec=0&startRow=401

        response = requests.get(base_url + queryProvince + queryYear + queryStartRow) # Using requests to read the HTML source
        
        ##print("##at fSoupFrames, URL to parse=", base_url + queryProvince + queryYear + queryStartRow)
        
        soup = BeautifulSoup(response.text, 'html.parser') # Parse with Beautiful Soup
        soup_frames.append(soup)
    return soup_frames
    


# In[5]:


#Example:
#sd='Sep2016'
#ed='Sep2017'

def lookUpStation(stationID, sd, ed, prov, name):
    
    print("****** at lookUpStation StationID=", stationID, " prov=", prov, "name=", name, "sd=", sd, "ed=", ed)
    
    start_date = datetime.strptime(sd, '%b%Y')
    end_date = datetime.strptime(ed, '%b%Y')

    frames = []
    ## here appends all WS of the province
    flagPC = True  ; print("at lookUpStation flagPC=", flagPC)
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    
        df, flagPC = getHourlyData(stationID, dt.year, dt.month, prov, name, flagPC) 
    
        print("################# dt.year=", dt.year, "dt.month=", dt.month)
    return df


# ################################################### main() #############################################################

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
    soup_frames = fSoupFrames(key, "2016", 10) ## need to supply year!


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
            prov = form.find("input", {"name" : "Prov"}) ['value'] ## added
            print(" ## conforming data by provinces with prov =", prov)
            if prov == "ON":
                # The stationID is a child of the form
                station = form.find("input", {"name" : "StationID"})['value']
            
                # The station name is a sibling of the input element named lstProvince
                name = form.find("input", {"name" : "lstProvince"}).find_next_siblings("div")[0].text
            
                # The intervals are listed as children in a 'select' tag named timeframe
                timeframes = form.find("select", {"name" : "timeframe"}).findChildren()
                intervals =[t.text for t in timeframes]
            
                # We can find the min and max year of this station using the first and last child
                years = form.find("select", {"name" : "Year"}).findChildren()            
                min_year = years[0].text
                max_year = years[-1].text
            
                ## print("#### min_year =", min_year, " #### max_year =", max_year)
            
                min_year = max_year ## just to consider the most recent year of measurements available
            
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


## changed from hourly to Monthly Data!!
# include
# Show only data with monthly intervals ; Im interested on this as I will be extracting only monthly data!
# 

hourly_stations = stations_df.loc[stations_df['Intervals'].map(lambda x: 'Hourly' in x)]
hourly_stations.to_csv('h_stations.csv') ## saving stations data with hourly data
hourly_stations.head()


# In[10]:


## Here iterate over all monthly stations in all provinces

## not needed allPframes = []
val = True

if os.path.exists("./fHourlyEC.csv"):
    os.remove("./fHourlyEC.csv")
    print("*** allSallP file DELETED ***")
else:
    print("The file does not exist")
        
for index, row in hourly_stations.iterrows():
    print (row["StationID"])
    print (row["Province"])
    print (row["Name"]) 
    ## here is not! print (row['Postal Code'])
    allStations = lookUpStation(row["StationID"], 'Jan2017', 'Dec2018', 
                                row["Province"], row["Name"]) 
