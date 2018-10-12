# coding: utf-8

# # Exploring Environment Canada Weather Data
# 
# This notebook demonstrates how to download Environment Canada's weather data using Python with popular data analysis libraries like pandas and Beautiful Soup.
# 
# Here import all necessary libraries
# 
# For new installations, use !pip install <pkg> --user 
# as a line of code to install missing packages
#     
# Adapted to extract Ontario and Toronto data: By J. Lopez
# 
# This version includes the province

# In[59]:


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


# In[60]:


# Store each page in a list and parse them later
soup_frames = []
stations_df = [] 


# function that takes in a station ID, the year and month and returns a pandas DataFrame with the downloaded data:

# In[61]:


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
    


# In[62]:


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
    soup_frames = fSoupFrames(key, "2015", 10)


# In[ ]:


#test!! do not run!!
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


# Each Weather Station is called a "row", startRow has the number of the starting row in each page, he assumes 100 pages or "rows" per page..
# 
# The soup currently goes nowhere..
# 
# how to determine max_pages?
# 
# This is only the list of stations where to find further information.

# Next the data frame will be saved in csv format

# This is an example of the URL that needs to be conformed to query EC for historical data
# 
# http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=2017&EndYear=2018&Year=2018&Month=1&Day=1&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&startRow=101

# Here loops to each station, gets the stationID, data intervals available for start and end years

# In[64]:


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
stations_df.head()


# In[65]:


# include
# Show only data with hourly intervals ; Im interested on this as I will be extracting only hourly data!
# 

hourly_stations = stations_df.loc[stations_df['Intervals'].map(lambda x: 'Hourly' in x)]
hourly_stations.head()


# In[66]:


hourly_stations.to_csv('h_stations.csv') ## saving stations data with hourly data


# In[86]:


#test
#hourly_stations["StationID"]

hourly_stations.iloc[2]


# In[101]:


# I will convert this into a function
#sd='Sep2016'
#ed='Sep2017'
def lookUpStation(stationID, sd, ed):
    start_date = datetime.strptime(sd, '%b%Y')
    end_date = datetime.strptime(ed, '%b%Y')

    frames = []
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        df = getHourlyData(stationID, dt.year, dt.month)
        frames.append(df)

    allStations = pd.concat(frames)
    allStations['Date/Time'] = pd.to_datetime(allStations['Date/Time'])
    allStations['Temp (°C)'] = pd.to_numeric(allStations['Temp (°C)'])
    #allStations.head(50)
    return allStations


# In[102]:


for index, row in hourly_stations.iterrows():
    print (row["StationID"])
    allStations = lookUpStation(row["StationID"], 'Sep2016', 'Sep2017')
    frames.append(allStations) ## aggregating all stations for all provinces!


# In[103]:


allStations.to_csv("allSallP.csv")


# In[100]:


#test OK OK OK OK OK
##for index, row in df.iterrows():
##    print (row["name"], row["age"])

for index, row in hourly_stations.iterrows():
    print (row["StationID"])


# In[67]:


# Do not execute!
# just an example of what I gotta save in the db!

#Get Toronto weather data for September 2002 to September 2017
# This is the data more suitable to be saved in a db

stationID = 31688 ## must iterate over each wstation

start_date = datetime.strptime('Sep2016', '%b%Y')
end_date = datetime.strptime('Sep2017', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

toronto = pd.concat(frames)
toronto['Date/Time'] = pd.to_datetime(toronto['Date/Time'])
toronto['Temp (°C)'] = pd.to_numeric(toronto['Temp (°C)'])
toronto.head(50)


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

# # Plotting the Data

# In[68]:



get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# # Interpolating missing points

# In[69]:


# Find the number of rows with a 'M' for missing temperature flag, or NaN for the actual temperature value
print('Missing data rows before interpolating: ', toronto.loc[(~toronto['Temp Flag'].isnull()) | (toronto['Temp (°C)'].isnull())].shape[0])

# Do interpolation 
toronto['Temp (°C)'] = toronto['Temp (°C)'].interpolate()

# Did we fix everything?
print('Missing data rows after interpolating : ', toronto.loc[(toronto['Temp (°C)'].isnull())].shape[0])


# reploting the data

# In[70]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# Exporting Data
# We'll export the dataframes in CSV format so we don't have to re-download the data every time we restart Jupyter:

# In[71]:


stations_df.to_csv('stations.csv')
toronto.to_csv('toronto.csv')

