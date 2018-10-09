
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import rrule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from fuzzywuzzy import fuzz


# In[2]:


# Call Environment Canada API
# Returns a dataframe of data
def getHourlyData(stationID, year, month):
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    api_endpoint = base_url + query_url
    return pd.read_csv(api_endpoint, skiprows=15)


# In[3]:


stationID = 31688
start_date = datetime.strptime('Jun2017', '%b%Y')
end_date = datetime.strptime('Jun2018', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

weather_data = pd.concat(frames)
weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'])
weather_data['Temp (°C)'] = pd.to_numeric(weather_data['Temp (°C)'])


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# In[5]:



# Don't really care about accuracy right now, use simple linear interpolation
weather_data['Temp (°C)'] = weather_data['Temp (°C)'].interpolate()


# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(weather_data['Date/Time'], weather_data['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# In[8]:


2+2


# In[7]:



# Specify Parameters
province = "ON"      # Which province to parse?
start_year = "2018"  # I want the results to go back to at least 2006 or earlier
max_pages = 2        # Number of maximum pages to parse, EC's limit is 100 rows per page, there are about 500 stations in BC with data going back to 2006

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


# http://climate.weather.gc.ca/historical_data/search_historic_data_stations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=2017&EndYear=2018&Year=2018&Month=1&Day=1&selRowPerPage=100&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&startRow=101

# In[9]:


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


# In[10]:


# Show only data with hourly intervals
hourly_stations = stations_df.loc[stations_df['Intervals'].map(lambda x: 'Hourly' in x)]
hourly_stations.head()


# In[13]:


# Find the stations that are in Whistler
string = "London"
tolerance = 90

hourly_stations[hourly_stations['Name'].apply(lambda x: fuzz.token_set_ratio(x, string)) > tolerance]


# In[12]:


# Find the stations that are in Toronto
string = "Toronto"
tolerance = 90

hourly_stations[hourly_stations['Name'].apply(lambda x: fuzz.token_set_ratio(x, string)) > tolerance]


# In[15]:


# Get Toronto weather data for November 2016 to November 2017
stationID = 31688
start_date = datetime.strptime('Nov2016', '%b%Y')
end_date = datetime.strptime('Nov2017', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

toronto = pd.concat(frames)
toronto['Date/Time'] = pd.to_datetime(toronto['Date/Time'])
toronto['Temp (°C)'] = pd.to_numeric(toronto['Temp (°C)'])
toronto.head()


# In[16]:



get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
fig = plt.figure(figsize=(15,5))
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'], '-o', alpha=0.8, markersize=2)
plt.plot(toronto['Date/Time'], toronto['Temp (°C)'].rolling(window=250,center=False).mean(), '-k', alpha=1.0)
plt.ylabel('Temp (°C)')
plt.xlabel('Time')
plt.show()


# # Interpolating missing points

# In[17]:


# Find the number of rows with a 'M' for missing temperature flag, or NaN for the actual temperature value
print('Missing data rows: ', toronto.loc[(~toronto['Temp Flag'].isnull()) | (toronto['Temp (°C)'].isnull())].shape[0])

# Do interpolation 
toronto['Temp (°C)'] = toronto['Temp (°C)'].interpolate()

# Did we fix everything?
print('Missing data rows: ', toronto.loc[(toronto['Temp (°C)'].isnull())].shape[0])


# reploting the data

# In[18]:


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

# In[19]:


stations_df.to_csv('stations.csv')
toronto.to_csv('toronto.csv')

