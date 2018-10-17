
# coding: utf-8

# # Exploring Environment Canada Weather Data
# 
# This notebook demonstrates how to scrape Environment Canada's weather data using Python with data analysis libraries like pandas and Beautiful Soup.
# 
# Here import all necessary libraries
# 
# For new installations, use !pip install <pkg> --user 
# as a line of code to install missing packages
#     
# Adapted to extract Ontario and Toronto data: By J. Lopez
# 
# This version includes the province

# In[85]:



# Call Environment Canada API
# Returns a dataframe of data
def getHourlyData(stationID, year, month, prov, name):
    print("at ############### getHourlyData with", year, month, prov, name)
    global val
    
    
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    URL = base_url + query_url
    time.sleep(2) ## This delay is necessary otherwise the program crashes!! ################################
    ## read URL
    import urllib.request
    with urllib.request.urlopen(URL) as response:
        station = response.read()
    ## Decode
    sin = station.decode('utf-8')
    sAll = [s.strip() for s in sin.splitlines()]

    # manipulate sAll[3] and sAll[4] to extract geoloc
    
    start = sAll[2].find('latitude/",/"') +13
    end = sAll[2].find('/"')
    lat = sAll[2][start:end]
    
    start = sAll[3].find('longitude/",/"') +14
    end = sAll[3].find('/"')
    lng = sAll[3][start:end]
    
    
    sDet = sAll[16:] ## extract hourly data, problem was here, data starts at row 16!!
    
    oCols=["Date/Time",
         "Year",
         "Month",
         "Day",
         "Time",
         "Temp (°C)",
         "Temp Flag",
         "Dew Point Temp (°C)",
         "Dew Point Temp Flag",
         "Rel Hum (%)",
         "Rel Hum Flag",
         "Wind Dir (10s deg)",
         "Wind Dir Flag",
         "Wind Spd (km/h)",
         "Wind Spd Flag",
         "Visibility (km)",
         "Visibility Flag",
         "Stn Press (kPa)",
         "Stn Press Flag",
         "Hmdx",
         "Hmdx Flag",
         "Wind Chill",
         "Wind Chill Flag",
         "Weather",
         "DUMMY-25"
          ]
    
    #test OK to split each row by ","
    lst = []
    df = [] ## init df
    
    for i in range(len(sDet)):
        new_sDet = str(sDet[i].replace("\"", "")).split(",")    
        lst.append(new_sDet) ## added
        print("new_sDet of ", i, "=", new_sDet)
        print("len(lst[", i, "][:])=", len(lst[i][:]))
        
        ##print("new_sDet=", new_sDet)
        
    print("len(oCols)=", len(oCols))
    print("len(lst[0])=", len(lst[0]))
    print("oCols[0:len(lst[0])]=", oCols[0:len(lst[0])])
    print("len of oCols[0:len(lst[0])]=", len(oCols[0:len(lst[0])]))
    
    print("################ out of for to build lst ######################")
    
    df = pd.DataFrame(lst, columns= oCols[0:len(lst[0])]) ## 24 columns converted!! problem is here!! [0:23] added
    
    ##################################################################################
    ## no longer needed df = pd.read_csv(api_endpoint, skiprows=15)
    ##################################################################################
    
    df['StationID'] = stationID
    df['Province'] = prov
    df['Name'] = name
    df['Latitude']= lat
    df['Longitude']= lng
    df['Postal Code']="X9X X9X"
    
    ## Rearrange columns
    
    ## rearranging columns
    df = df[['Province', 
             'StationID', 
             'Name', 
             'Latitude', 
             'Longitude', 
             'Postal Code', 
             'Year',
             'Month',
             'Day',
             'Time',
             'Temp (°C)',
             'Dew Point Temp (°C)',
             'Wind Dir (10s deg)',
             'Wind Spd (km/h)',
             'Visibility (km)',
             'Stn Press (kPa)',
             'Weather']]

    with open('allSallP.csv', 'a') as f:
        df.to_csv(f, header=val, index = True) ## just for testing changed!!
        print("###### header=", val)
    val = False
    return df


# In[19]:


#TEST

oCols=["Date/Time",
         "Year",
         "Month",
         "Day",
         "Time",
         "Temp (°C)",
         "Temp Flag",
         "Dew Point Temp (°C)",
         "Dew Point Temp Flag",
         "Rel Hum (%)",
         "Rel Hum Flag",
         "Wind Dir (10s deg)",
         "Wind Dir Flag",
         "Wind Spd (km/h)",
         "Wind Spd Flag",
         "Visibility (km)",
         "Visibility Flag",
         "Stn Press (kPa)",
         "Stn Press Flag",
         "Hmdx",
         "Hmdx Flag",
         "Wind Chill",
         "Wind Chill Flag",
         "Weather"]


# In[68]:


lst


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
    


# Next the data frame will be saved in csv format

# This is an example of the URL that needs to be conformed to query EC for historical data
# 
# http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=2017&EndYear=2018&Year=2018&Month=1&Day=1&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&startRow=101

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
    
        df = getHourlyData(stationID, dt.year, dt.month, prov, name) ## what for df then???
        print("################# dt.year=", dt.year, "dt.month=", dt.month)
        
        ##frames.append(df) ## why use append here? ## needed???
    
    ##allStations = pd.concat(frames) ## and concat here? ## needed???
    
    ##allStations['StationID'] = stationID
    ##allStations['Province'] = prov
    ##allStations['Name'] = name
    
    
    ###### NO NEED ########### df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    ## df['Temp (°C)'] = pd.to_numeric(df['Temp (°C)'])   conversion may not be needed for now.. 
    ##################################
    #allStations.head(50)
    ##return allStations
    return df


# # Data Explanation:
# 
# # temperature (°C)
# The temperature of the air in degrees Celsius (°C). At most principal stations the maximum and minimum temperatures are for a day beginning at 0600 Greenwich (or Universal) Mean Time, which is within a few hours of midnight local standard time in Canada.
# 
# # dew point temperature (°C)
# The dew point temperature in degrees Celsius (°C), a measure of the humidity of the air, is the temperature to which the air would have to be cooled to reach saturation with respect to liquid water. Saturation occurs when the air is holding the maximum water vapour possible at that temperature and atmospheric pressure.
# 
# # relative humidity (%)
# Relative humidity in percent (%) is the ratio of the quantity of water vapour the air contains compared to the maximum amount it can hold at that particular temperature.
# 
# # wind speed (km/h)
# The speed of motion of air in kilometres per hour (km/h) usually observed at 10 metres above the ground. It represents the average speed during the one-, two- or ten-minute period ending at the time of observation. In observing, it is measured in nautical miles per hour or kilometres per hour.
# 
# Conversion factors:1 nautical mile = 1852 metres or 1.852 km
# therefore1 knot = 1.852 km/h
# and1 km/h = 0.54 knot.
# 
# # visibility (km)
# Visibility in kilometres (km) is the distance at which objects of suitable size can be seen and identified. Atmospheric visibility can be reduced by precipitation, fog, haze or other obstructions to visibility such as blowing snow or dust.
# 
# # station pressure (kPa)
# The atmospheric pressure in kilopascals (kPa) at the station elevation. Atmospheric pressure is the force per unit area exerted by the atmosphere as a consequence of the mass of air in a vertical column from the elevation of the observing station to the top of the atmosphere.
# 
# # Hmdx column and on are NaN

# In[5]:


##################################################### main() ##################################################################


# In[62]:


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

val = True


# In[7]:


# Store each page in a list and parse them later
soup_frames = []
stations_df = [] 


# In[8]:


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

# In[9]:


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


# In[10]:


# include
# Show only data with hourly intervals ; Im interested on this as I will be extracting only hourly data!
# 

hourly_stations = stations_df.loc[stations_df['Intervals'].map(lambda x: 'Hourly' in x)]
hourly_stations.to_csv('h_stations.csv') ## saving stations data with hourly data
hourly_stations.head()


# In[87]:


#just test with one ws
val = True
allStations = lookUpStation("31688", 'Sep2016', 'Sep2017', "ON", "TORONTO CITY")


# In[86]:


## Here iterate over all hourly stations in all provinces

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
    allStations = lookUpStation(row["StationID"], 'Sep2016', 'Sep2017', 
                                row["Province"], row["Name"]) 
    ## What period of information we want?, the longer the period the bigger the data will generate!
    ##nnallPframes.append(allStations) ## aggregating all stations for all provinces!

