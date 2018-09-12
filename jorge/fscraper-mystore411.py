
# coding: utf-8

# Program: fscraper-mystore411.py
# 
# Author. Jorge Lopez
# 
# Date. 9/3/18
# 
# Input: A store name (present in Canada)
# 
# Output: Coordinates lat, long using Google API
# 
# This Program has the purpose to scrape the website mystore411.com using the help of BeautifulSoup
# 
# Provided a store name, the program retrieves the associated URL for all the locations where the store is present
# 
# For each store URL, uses Gopy to retrieve its coordinates (lat and long)
# 
# Automatically retrieves the store ID from the store name inputted
# 

# In[40]:


# initializations

## already reading it! storeName = 'Acura'
## url = "https://mystore411.com/store/category/Car+Dealer"

#loading of library to read website

import urllib2
import requests


# In[41]:


## these two lines to avoid the SSL error
import ssl
context = context = ssl._create_unverified_context()


# In[42]:


def getStoreID(StoreName):
    
    # here reads the top biz url!
    store = urllib2.urlopen(url,context = context)
    #import the Beautiful soup functions to parse the data returned from the website
    from bs4 import BeautifulSoup
    #Parse the html in the 'store' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(store)

    print("In getstoreID f")
    ## Get the store ID for storeName
    sid = "XXX"
    for a in soup.find_all("a", href=True):
        if storeName in a['href']:
            urlSID = str(a['href'])
            start = urlSID.find("listing/") + 8
            end = urlSID.find('/', start)
            sid = urlSID[start:end]
            print("getStoreID URL is", a['href']) 
            print("getstoreID Found id is ", sid)
            break ## ends for
    return sid


# In[43]:


def getGeoloc(add):
    
    ## get coordinates of address
    
    param = {'address': add, 'key': 'AIzaSyCahybZqELJlJAWmQ3p-dTRBlNtuLfHr34'}

    response = requests.get(geo_s, params=param)

    json_dict = response.json()

    ## testing
    lat = json_dict['results'][0]['geometry']['location']['lat']
    lng = json_dict['results'][0]['geometry']['location']['lng']
    
    ll = str(lat) + "," + str(lng)
    
    return ll


# In[44]:


def getAddress(storeURL):
    store = urllib2.urlopen(storeURL,context = context)
    soup = BeautifulSoup(store)
    print(storeURL)
    ## conforming address
    span = str(soup.find_all("span",itemprop="streetAddress"))
    start = span.find("Address>") + 33
    end = span.find('<br', start)
    address = span[start:end]
    ## addressLocality
    span = str(soup.find_all("span",itemprop="addressLocality"))
    start = span.find("Locality") + 10
    end = span.find('</span>', start)
    loc = span[start:end]
    ## addressRegion
    span = str(soup.find_all("span",itemprop="addressRegion"))
    start = span.find("Region") + 8
    end = span.find('</span>', start)
    reg = span[start:end]
    ## postalCode
    span = str(soup.find_all("span",itemprop="postalCode"))
    start = span.find("Code") + 6
    end = span.find('</span>', start)
    pos = span[start:end]
        
    add = address + " " + loc + " " + reg + " " + pos
    
    return add


# In[45]:


## TESTING BLOCK TO RETRIEVE BIZ CATEGORY (2) EXECUTE

def getCategory(category):
        
    url = "https://mystore411.com"

    store = urllib2.urlopen(url,context = context) ## first url with category
    print("url for top biz is", url)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store)
    
    ## print(soup)
    
    for a in soup.find_all("a", href=True):
        
        print("category is", category)
        print("a[href] is", a['href'])
        
        if category in a['href']:
            
            urlCID = "http://mystore411.com" + str(a['href'])
            print("a[href]=", a['href'])
            print("urlCID=", urlCID)
            print("getCategory URL is", "http://mystore411.com" + a['href']) 
    
            start = urlCID.find("category/") + 9
    
            print("start is", start)
    
            cid = urlCID[start:]
    
            print("getCategory Found id is ", cid)
        
            break
        else:
            cid = "X"
            
    return cid


# In[46]:


def getAddfromLL(ll):
    from geopy.geocoders import GoogleV3

    ##point = '52.157927, -106.660661' #
    ##print("ll from getAddfromLL is ", ll)

    geolocator = GoogleV3(api_key = 'AIzaSyCahybZqELJlJAWmQ3p-dTRBlNtuLfHr34')
    address = geolocator.reverse(ll)
    
    address = address[0]
    
    print("REVERSAL The address of ", ll, "is:")
    print address[0]
    
    return address
    


# In[48]:


## main()

#category = raw_input('Enter a valid business category in mystore411.com: ') ## not used to validate anything
#print("category is " + category)

#storeName = raw_input('Enter a valid store Name in mystore411.com: ')
#print('storeName is '+  storeName)

#url = "https://mystore411.com"

#store = urllib2.urlopen(url,context = context) ## first url with category
#print("url for top biz is", url)
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(store)

cid = "X"
while cid == "X":
    category = raw_input('WHILE Enter a valid business category in mystore411.com: ') ## not used to validate anything
    print("category is " + category)
    cid = getCategory(category)
    if cid != "X":
        print("OK category found!:", cid)
    


# In[49]:



print("category is " + category)

url = "https://mystore411.com/store/category/" + category 



# here reads the top biz url!
#store = urllib2.urlopen(url,context = context)
#import the Beautiful soup functions to parse the data returned from the website
#from bs4 import BeautifulSoup
#Parse the html in the 'store' variable, and store it in Beautiful Soup format
#soup = BeautifulSoup(store)

sid = "XXX"
while sid == "XXX":
    storeName = raw_input('Enter a valid store Name in mystore411.com: ')
    print('storeName is '+  storeName)
    sid = getStoreID(storeName)
    if sid != "XXX":
        print("StoreID for ", storeName, " has been found")
        #specify the url
        url = str('http://www.mystore411.com/store/listing/' + sid + '/Canada/' + storeName + '-store-locations')
        print(url)

        ## initializations to get the geolocation of the address of the storeName
        geo_s = 'https://maps.googleapis.com/maps/api/geocode/json'



# In[50]:


## Itererate over the storeName url and compose the address

store = urllib2.urlopen(url,context = context) ## first url with category
print("url for top biz is", url)
from bs4 import BeautifulSoup
soup = BeautifulSoup(store)
##

for a in soup.find_all('a',href=True):
   if "view" in a['href']:
    storeURL = ('http://mystore411.com' + a['href']).encode('utf-8')
    store = urllib2.urlopen(storeURL,context = context)
    soup = BeautifulSoup(store)
    ## print(storeURL)
    ## conforming address
    add = getAddress(storeURL)
    print(add)
    ##ll = getGeoloc(add).encode('ascii', 'ignore') ## 5625 Boul. M\xe9tropolitain St-L\xe9onard Quebec H1P 1X3  This may not be working
    ll = getGeoloc(add)
    print("lat and long are:", ll)
    
    ## also, given a lat and lng we can extract the address
    
    add = getAddfromLL(ll)
    
    ## print("Address for ", ll, " is ", add)
    

