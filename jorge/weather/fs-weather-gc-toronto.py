
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
# Adapted to extract Ontatio and Toronto data: By J. Lopez

# In[54]:


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


# function that takes in a station ID, the year and month and returns a pandas DataFrame with the downloaded data:

# In[55]:


# Call Environment Canada API
# Returns a dataframe of data
def getHourlyData(stationID, year, month):
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    api_endpoint = base_url + query_url
    return pd.read_csv(api_endpoint, skiprows=15)


# To get data for a given period we just need to create a loop to grab the individual DataFrames and then use pd.concat to merge it all together.
# 
# For instance if we would like to collect weather data from June 2015 to June 2016? Instead of writing some awkward loops to get the correct months we can use the datetime and dateutil libraries to help us.
# 
# Using rrule, which is part of dateutil, we can loop through the correct months easily just by defining a start date and and ending date and using the rrule.MONTHLY frequency:

# In[56]:


stationID = 31688 ## This is Toronto station
start_date = datetime.strptime('Jun2017', '%b%Y')
end_date = datetime.strptime('Jun2018', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

weather_data = pd.concat(frames)
weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'])
weather_data['Temp (°C)'] = pd.to_numeric(weather_data['Temp (°C)'])


# Plot average data and a rolling average
# 
# The broken lines, they indicate missing data points.

# In[57]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# In[58]:


fwd_o = weather_data['Temp (°C)']


# In[59]:


fwd_o.to_csv(r'./fwd_o.txt', header=None, index=None, sep=',', mode='a')


# In[60]:


# use simple linear interpolation to complete missing data
weather_data['Temp (°C)'] = weather_data['Temp (°C)'].interpolate()


# In[61]:


fwd_i.to_csv(r'./fwd_i.txt', header=None, index=None, sep=',', mode='a')


# In[62]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# Each Weather Station is called a "row", startRow has the number of the starting row in each page, he assumes 100 pages or "rows" per page..
# 
# The soup currently goes nowhere..
# 
# how to determine max_pages?
# 
# This is only the list of stations where to find further information.

# In[63]:


## I don't get exactly what this is for

# Specify Parameters
province = "ON"      # Which province to parse?
start_year = "2015"  # I want the results to go back to at least this year or earlier
max_pages = 100        # Number of maximum pages to parse, EC's limit is 100 rows per page

# Store each page in a list and parse them later
soup_frames = []

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
    
    


# Next the data frame will be saved in csv format

# This is an example of the URL that needs to be conformed to query EC for historical data
# 
# http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=2017&EndYear=2018&Year=2018&Month=1&Day=1&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&startRow=101

# Here loops to each station, gets the stationID, data intervals available for start and end years

# In[64]:


# Empty list to store the station data
station_data = []

for soup in soup_frames: # For each soup
    forms = soup.findAll("form", {"id" : re.compile('stnRequest*')}) # We find the forms with the stnRequest* ID using regex 
    for form in forms:
        try:
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
            
            # Store the data in an array
            data = [station, name, intervals, min_year, max_year]
            station_data.append(data)
        except:
            pass

# Create a pandas dataframe using the collected data and give it the appropriate column names
stations_df = pd.DataFrame(station_data, columns=['StationID', 'Name', 'Intervals', 'Year Start', 'Year End'])
stations_df.head()


# In[65]:


# Show only data with hourly intervals
# 

hourly_stations = stations_df.loc[stations_df['Intervals'].map(lambda x: 'Hourly' in x)]
hourly_stations.head()


# In[66]:


# Find the stations that are in London
string = "London"
tolerance = 90

hourly_stations[hourly_stations['Name'].apply(lambda x: fuzz.token_set_ratio(x, string)) > tolerance]


# In[68]:


# Find the stations that are in Toronto; same as above 
string = "Toronto"
tolerance = 90

hourly_stations[hourly_stations['Name'].apply(lambda x: fuzz.token_set_ratio(x, string)) > tolerance]


# In[69]:


hourly_stations.head()


# In[70]:


## Example of using fuzzywuzzy 

fuzz.token_set_ratio("Jorge A Lopez", "Jorge Arturo L.")


# In[71]:


# Get Toronto weather data for September 2002 to September 2017
# This is the data more suitable to be saved in a db
stationID = 31688
start_date = datetime.strptime('Sep2016', '%b%Y')
end_date = datetime.strptime('Sep2017', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

toronto = pd.concat(frames)
toronto['Date/Time'] = pd.to_datetime(toronto['Date/Time'])
toronto['Temp (°C)'] = pd.to_numeric(toronto['Temp (°C)'])
toronto.head()


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

# In[72]:



get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# # Interpolating missing points

# In[73]:


# Find the number of rows with a 'M' for missing temperature flag, or NaN for the actual temperature value
print('Missing data rows before interpolating: ', toronto.loc[(~toronto['Temp Flag'].isnull()) | (toronto['Temp (°C)'].isnull())].shape[0])

# Do interpolation 
toronto['Temp (°C)'] = toronto['Temp (°C)'].interpolate()

# Did we fix everything?
print('Missing data rows after interpolating : ', toronto.loc[(toronto['Temp (°C)'].isnull())].shape[0])


# reploting the data

# In[74]:


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

# In[75]:


stations_df.to_csv('stations.csv')
toronto.to_csv('toronto.csv')

