
# coding: utf-8

# Program: find-nearest-ws.py
# 
# Author. J. Lopez
# 
# This program finds the nearest weather station according to their coordinates to a given postal code supplied by the user in format "MXM MXM".
# 
# The programs looks for the weather stations in the "weather-stations" table of the database "weather" residing in this VM, according to the first letter of the postal code entered, locates all the weather stations in the table that matches that letter. Then use Geopy to calculate the distance between the postal code entered and each postal code found in the database (using the coordinates of the postal codes).
# 

# In[52]:


import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBCStYlYkMxdXJYJjuVEINvU7U8HBarCJ0'

import geocoder


# In[53]:


connection = psycopg2.connect(database='weather', user='postgres', password='postgres', host='localhost')


# In[54]:


cursor = connection.cursor()


# In[55]:


cursor.execute("SELECT postal_code, province, lati_tude, longi_tude FROM weather_table")


# In[56]:


outputR = cursor.fetchall()


# In[57]:


outputR


# In[58]:


pc = input("Enter the Postal code in format X9X X9X:")


# In[60]:


m = input("What MONTH you would like to find what the weather is like at this location? [1-12]:")


# In[61]:


firstLetterPC = pc[0:1]


# In[62]:


##cur.execute("SELECT postal_code, province, lati_tude, longi_tude FROM weather_table where postal_code like M%", (pc[0:1]))

stmt= "SELECT station, postal_code, province, lati_tude, longi_tude, year, month, mean_temp_c          FROM weather_table where month = %s AND postal_code like '%s%%'" % ( m, firstLetterPC ) 

print stmt
cursor.execute( stmt )

#cur.execute(" like '%%s%'")


# In[63]:


outputR = cursor.fetchall()


# In[65]:


outputR


# In[66]:


#cols = ['postal code', 'province', 'lat', 'lng', 'Temp C']
cols = ['station', 'postal_code', 'province', 'lati_tude', 'longi_tude', 'year', 'month', 'mean_temp_c']
df = pd.DataFrame(outputR, columns= cols)


# In[67]:


df


# In[46]:


################################################# main() ######################################################


# In[68]:


geolocIn = getInPCgeol(pc)


# In[69]:


geolocIn


# In[70]:


def calcDistance(lat1,lng1,lat2,lng2):
    import geopy.distance
    coords_1 = (lat1, lng1)
    coords_2 = (lat2, lng2)
    return geopy.distance.vincenty(coords_1, coords_2).km


# In[71]:


def compPCds(df):
    i=0
    d=[]
    while i < len(df):
        if not(math.isnan(df.iloc[i,7])):   
            print("i=",i, df.at[i,'station'], " is not NAN")
            distance = calcDistance(geolocIn[0], geolocIn[1], df.iloc[i,3], df.iloc[i,4])
            d.append(distance)
            print("the distance between", pc, "and station ", df.at[i,'station'],                   "located at", df.at[i,'postal_code'], "is at ", distance, "Kms.")
        i+=1
        print(d)
    return min(d)


# In[72]:


mini = compPCds(df)

print("Therefore the closest postal code to", pc, "is", mini )


# In[ ]:


################################################### TESTING FROM HERE ##############################################

