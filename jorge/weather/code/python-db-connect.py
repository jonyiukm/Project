
# coding: utf-8

# This program connects to the PostgreSQL database and finds the closest weather station postal code of a postal code
# Authir. J. Lopez

# In[1]:


#TEST OK
import psycopg2


# In[2]:


##TEST OK for connecting to SQL CLOUD
##conn = psycopg2.connect(database='postgres', user='postgres', password='cloudsql', host='35.224.133.152', port='5432')


# In[3]:


#TEST TO CONECT TO localhost database
conn = psycopg2.connect(database='weather', user='postgres', password='postgres', host='localhost')


# In[4]:


cur = conn.cursor()


# In[5]:


cur.execute("SELECT postal_code, province, lati_tude, longi_tude FROM weather_table")


# In[6]:


rows = cur.fetchall()


# In[7]:


rows


# In[8]:


pc = input("Enter the Postal code in format X9X X9X:")


# In[9]:


var1=pc[0:1]


# In[16]:


##cur.execute("SELECT postal_code, province, lati_tude, longi_tude FROM weather_table where postal_code like M%", (pc[0:1]))

stmt= "SELECT postal_code, province, lati_tude, longi_tude FROM weather_table where postal_code like '%s%%'" % ( var1 )
print stmt
cur.execute( stmt )

#cur.execute(" like '%%s%'")


# In[17]:


rows = cur.fetchall()


# In[18]:


rows

