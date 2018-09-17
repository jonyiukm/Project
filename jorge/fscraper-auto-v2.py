
# coding: utf-8

# Program: fscraper-mystore411.py
# 
# Author. Jorge Lopez
# 
# Dates. 9/3/18, 9/14/18, 9/16/18
# 
# Input: The website mystore411.com
# 
# Output: Coordinates lat, long using Google API of all the Canadian businesses found
# 
# This Program has the purpose to scrape the website mystore411.com using the help of BeautifulSoup
# 
# Automatically retrieves all businesses locations in Canada

# In[1]:


# initializations

import urllib2
import requests
import time
import sys
import datetime


# In[ ]:


## THIS CODE MUST BE EXECUTED!!
## these two lines to avoid the SSL error
import ssl
context = context = ssl._create_unverified_context()


# In[ ]:


def getCategories(lCat):
    ## print("in getCategories")
    ## print("inCategories href=", a['href'])
    
    if "category" in a['href']:
        
        urlCID = "http://mystore411.com" + str(a['href'])
        
        ##print("a[href]=", a['href'])
        ##print("urlCID=", urlCID)
        start = urlCID.find("category/") + 9
        cid = urlCID[start:] ## what for?
        ##print("getCategory Found id is ", cid) ## what for?
        
        lCat.append(urlCID)
        
        ## print("This is the dictionary of categories inside getCategories:", dCat)
            
    return lCat


# In[ ]:


def getBusinesses(url):
    print("*********** at getBusinesses url is:", url)
    
    lBiz =[]
  
    store = urllib2.urlopen(url,context = context)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store) 
    
    StoreList = str(soup.find_all("a", href=True)).split(",")

    for i in range(0,len(StoreList)):
        if ("store" and "listing" and "Canada") in StoreList[i]: ## separates ifs??
        
            start = StoreList[i].find('listing/') + 8
            end = StoreList[i].find('-store', start)
            biz = StoreList[i][start:end]
                                  
            ##print("Biz=", Biz)
            
            url = "https://www.mystore411.com/store/listing/" + biz + "-store-locations"
            
            ## print("url of biz found is:", url)
            
            lBiz.append(url)
            
    return lBiz;


# In[ ]:


def getCities(url):
    print("************** at getCities URL is", url)
    lCity = []
    store = urllib2.urlopen(url,context = context)
    time.sleep(2) ## This delay is necessary otherwise the program crashes!!
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store) 
    print(">>>>>>>>>>>>> at getCities after urlopen and creating the soup")
    if soup.find("th", colspan="3"): ## this means there are Cities in the Province
        CityList = str(soup.find_all("a", href=True)).split(",")
        for i in range(0,len(CityList)):
            if "/Canada/" in CityList[i]: ## important need to look for Canada/ because Canada is sometime embedded in name
                if "/list_city/" in CityList[i]:
                    ##print("CityList[", i, "=", CityList[i])
                    ##print(StoreList[i])
                    start = CityList[i].find('list_city/') + 10 ## strings start in [0] in python!
                    end = CityList[i].find('-store', start)
                    City = CityList[i][start:end]
                                  
                    ##print("City=", City)
            
                    url = "htpps://www.mystore411.com/store/list_city/" + City + "-store-locations" 
            
                    print("url of biz found is:", url)
            
                    lCity.append(url)
    else:
        print("For ", url, ", colspan not 3 perform getLocation(url)", url)
        getLocation(url)
        
    ##print("CityList=", lCity)
    return lCity


# In[ ]:


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


# In[ ]:


def getGeoloc(add):
    
    ## get coordinates of address
    
    param = {'address': add, 'key': 'AIzaSyCahybZqELJlJAWmQ3p-dTRBlNtuLfHr34'}
    geo_s = 'https://maps.googleapis.com/maps/api/geocode/json' ## needed
    
    response = requests.get(geo_s, params=param)

    json_dict = response.json()

    ## testing
    lat = json_dict['results'][0]['geometry']['location']['lat']
    lng = json_dict['results'][0]['geometry']['location']['lng']
    
    ll = str(lat) + "," + str(lng)
    
    time.sleep(2) ## this might be inefficient! 
    
    return ll


# In[ ]:


def getLocation(url):
    
    ##lLoc = [] ## I don't think you need to save the entry!!
    
    ## Here I read the business
    store = urllib2.urlopen(url,context = context) ## first url with category
    print("url for top biz is", url)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store)
    ##

    counter = 0
    for a in soup.find_all('a',href=True): 
        
        if "view" in a['href']:
            counter+=1 ## delete after testing!!!
            
            storeURL = ('https://mystore411.com' + a['href']).encode('utf-8') ## Here I conform the URL for reading the store name of the biz
            store = urllib2.urlopen(storeURL,context = context)
            soup = BeautifulSoup(store)

        ## conforming address
            add = getAddress(storeURL)
            print("The address of the biz is:", add)
        ##ll = getGeoloc(add).encode('ascii', 'ignore') ## 5625 Boul. M\xe9tropolitain St-L\xe9onard Quebec H1P 1X3  This may not be working
            ll = getGeoloc(add)
            print("lat and long are:", ll)
            
            if counter == 2: ## This constraint needs to be removed for production!!!
                print("DDDDDDDDDDDDDDDDDDD there are more than 2 view URLS then I break!!!")
                break


# In[ ]:


def getStates(url):
    print("******************* in getStates def for URL:", url)
    lStates = []
    store = urllib2.urlopen(url,context = context)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store)

    if soup.find("th", colspan="4"):
        
        ProvList = str(soup.find_all("a", href=True)).split(",")
        for i in range(0,len(ProvList)): ## decomment for production !!!
        ## for i in range(0,3): ## and I am risking that buz-cat has at least 3 locations!!!!
            if "/Canada/" in ProvList[i]: ## needs to be "Canada/" otherwise it mixes up with Canada-Goose-store-locations!!
                if "list_state" in ProvList[i]:
                    ##print("ProvList[", i, "=", ProvList[i])
                    ##print(StoreList[i])
                    start = ProvList[i].find('list_state/') + 11 ## strings start in [0] in python!
                    end = ProvList[i].find('-store', start)
                    prov = ProvList[i][start:end]
                                  
                    ##print("prov=", prov)
            
                    url = "https://www.mystore411.com/store/list_state/" + prov + "-store-locations" 
            
                    print("url of biz found is:", url)
            
                    lStates.append(url) ## will append only if the biz has states!
                
                    ## print("+++++++++++++++++++++++++after appending to lStates:", lStates)
                    
                    ## Here I might continue processing list_state but better I do itthrough the list
                
    else:
        ##Im not sure this is correct!!
        ## Given that url is already filtered out for Canada I think is correct!!!
        ## read location
        print("************** THERE is NO COLSPAN=4 for ", url, "*****************************")
        print("************** I will getLocation (url) ***************************************")
        getLocation(url)

    return lStates


# Main()
# 
# 1 Read all categories
# 
# 1 Read the URL for each category found on 1. to get the list of businesses
# 
# 3 Read each of the Businesses and test if it has State (Province) locations

# In[ ]:


url = "https://mystore411.com"

lCat   = []
lBiz   = []
lSta   = []
lCit   = []
lABiz  = []
lASta  = [] 
lACit  = []

print("top url is", url)

store = urllib2.urlopen(url,context = context)
from bs4 import BeautifulSoup
soup = BeautifulSoup(store)

print ("Process of scrapping website STARTS at:", datetime.datetime.now())
for a in soup.find_all('a',href=True): ## LOOK FOR ALL CATEGORIES  
    lCat = getCategories(lCat)
    
print("&&&&&&&&&&&&&& This is the list of categories:", lCat)

for i in range(0, len(lCat)):
##for i in range(0, 3): ## delete for production 
    lBiz = getBusinesses(lCat[i])
    lABiz += lBiz
print("&&&&&&&&&&&&&& This is the list of ALL Businesses in each category:", lABiz)

print(" =============================== in getStates =======================================")

for i in range(0, len(lABiz)):
##for i in range(0, 3):   ## delete for production 
    lSta = getStates(lABiz[i])
    lASta += lSta
print("&&&&&&&&&&&&&& This is the list of ALL States in each business:", lASta)

## writing lASta into a file for debugging purposes!!!!
f = open("./fscraper-lASta", "w")
for i in range(0,len(lASta)):
    f.write(lASta[i]+",")
f.close()

for i in range(0, len(lASta)):
##for i in range(0, 3):  ## delete for production  
    lCit = getCities(lASta[i])
    lACit += lCit
    print("%%%%%%%%%%%%%%% getlocation(lAsta[i]) %%%%%%%%%%%%%%%%%%% i=", i)

for i in range(0, len(lACit[i])): ## Here retrieve all store that are present in cities
    getLocation(lACit[i]) 

print("&&&&&&&&&&&&&& This is the list of Cities in each State:", lACit)

print ("Process of scrapping website ENDED at:", datetime.datetime.now())

## I still need to read all URLs of lACit[] !!!
## reversing the stdout and closing f
##sys.stdout = orig_stdout:/
###f.close()


