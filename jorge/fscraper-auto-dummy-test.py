# coding: utf-8

# Program: fscraper-mystore411.py
# 
# Author. Jorge Lopez
# 
# Dates. 9/3/18, 9/14/18, 9/16/18, 9/17/18
# 
# Input: The website mystore411.com
# 
# Output: Coordinates lat, long using Google API of all the Canadian businesses found
# 
# This Program has the purpose to scrape the website mystore411.com using the help of BeautifulSoup
# 
# Automatically retrieves all businesses locations in Canada
# 
# Conforms the output to build the database table containing:
# 
# Name, Address, City, Prov, Postal-Code, Latitude, Longitude, Rating and Types
# 
# This version is just to estimate the volume of the output!!
# 

# In[32]:


# initializations

import urllib2
import urllib
import requests
import time
import sys
import datetime
import csv
import os

from bs4 import BeautifulSoup


# In[33]:


## Global variables for output

OutName = " "
OutAdd  = " "
OutCity = " "
OutProv = " "
OutPost = " "
OutLat  = " "
OutLng  = " "
OutRtg  = " "
OutTyp  = " "

countw = 0


# In[34]:


## these two lines to avoid the SSL error
import ssl
context = context = ssl._create_unverified_context()


# In[35]:


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


# In[36]:


def getBusinesses(url):
    print("*********** at getBusinesses url is:", url)
    
    lBiz =[]
  
    store = urllib2.urlopen(url,context = context)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store, "lxml") 
    
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


# In[37]:


def getCities(url):
    print("************** at getCities URL is", url)
    lCity = []
    store = urllib2.urlopen(url,context = context)
    time.sleep(2) ## This delay is necessary otherwise the program crashes!!
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store, "lxml") 
    
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
            
                    url = "https://www.mystore411.com/store/list_city/" + City + "-store-locations" 
            
                    print("url of biz found is:", url)
            
                    lCity.append(url)
    else:
        print("For ", url, ", colspan not 3 will perform getLocation(url)", url)
        TGetLocation(url)
        
    ##print("CityList=", lCity)
    return lCity


# In[38]:


def getAddress(storeURL):
    global OutAdd  
    global OutCity
    global OutProv
    global OutPost
    
    store = urllib2.urlopen(storeURL,context = context)

    soup = BeautifulSoup(store, "lxml") ## this is wrong, not suppose to re-read!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    ##print(storeURL)
    ## conforming address
    span = str(soup.find_all("span",itemprop="streetAddress"))
    print "debugging span=", span
    start = span.find('Address') + 9
    end = span.find('<br', start)
    address = str(span[start:end]) + "" ## I am converting to string if I can get rid of ""
    ## addressLocality
    span = str(soup.find_all("span",itemprop="addressLocality")) ## City
    start = span.find("Locality") + 10
    end = span.find('</span>', start)
    loc = span[start:end]
    ## addressRegion
    span = str(soup.find_all("span",itemprop="addressRegion")) ## Province
    start = span.find("Region") + 8
    end = span.find('</span>', start)
    reg = span[start:end]
    ## postalCode
    span = str(soup.find_all("span",itemprop="postalCode"))
    start = span.find("Code") + 6
    end = span.find('</span>', start)
    pos = span[start:end]
        
    add = address + " " + loc + " " + reg + " " + pos
    
    ## conform table
    OutAdd  = address
    print "at getAddress ====== address is>", address, "<"
    OutCity = loc
    OutProv = reg
    OutPost = pos
    
    return add


# In[39]:


def getGeoloc(add):
    
    ## NOT USED!!!
    
    lat = 7.0
    lng = 9.0
    
    return str(lat), str(lng)


# In[40]:


def unlistTypes(types):
## remove unwanted characters from types
    l = str(types)
    s = l
    l = s
    rc = "[u\']"
    for i in range(0, len(rc)):
        if rc[i] in l:
            s = s.replace(rc[i],"")
        
    return s
        


# In[41]:


def getStates(url):
    print("******************* in getStates def for URL:", url)
    lStates = []
    store = urllib2.urlopen(url,context = context)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store, "lxml")

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
        ## Given that url is already filtered out for Canada I think is correct!!!
        ## read location
        print("************** THERE is NO COLSPAN=4 for ", url, "*****************************")
        print("************** I will GetLocation (url) ***************************************")
        TGetLocation(url)

    return lStates


# In[42]:


## these two lines to avoid the SSL error THIS IS OK
import ssl
context = context = ssl._create_unverified_context()


# In[43]:


## TEST REDUNDANT
import urllib2
import ssl

context = context = ssl._create_unverified_context()


# In[49]:


## TEST ## THIS IS THE NEW FUNCTION THAT WORKS!!! OK
def TGetLocation(url):

    print("at TGetLocation with url:", url)
    global countw
    
    ##try:
    time.sleep(2) ## introducing a delay to see if makes a difference!
    f = urllib.urlopen(url, context=context)
    store = f.read()
    ##except:
    ##print "############################### ERROR WHEN READING URL:", url
    ##return
    
    
    print("AFTER READING URL. url for top biz is", url)
   
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(store, "lxml")
    
    print("at TgetLocation ====== url for top biz is", url) 

    counter = 0
    for a in soup.find_all('a',href=True): 
        ## print("in for a[href] ======", a['href'])
        if "view" in a['href']:
            counter+=1 ## delete after testing!!!
            print("a[href] with (view) ====>>>>>>>", a['href'])
            ## by setting counter > 0 I'm opening the gates to full processing!!
            print("counter = ", counter)
            storeURL = ('https://mystore411.com' + a['href']).encode('utf-8') ## Here I conform the URL for reading the store name of the biz
            print("BEFORE ====== storeURL is:", storeURL, "a[href] is:", a['href'])
            if counter >= 1: ## delete for production!! just writing 1 for TESTING!!!! ##########################################
                
                storeURL = ('https://mystore411.com' + a['href']).encode('utf-8') ## Here I conform the URL for reading the store name of the biz
                print("at TGetLocation ====== storeURL is:", storeURL, "a[href] is:", a['href'])
                add = getAddress(storeURL)
                print("The address of the biz with is:", add)
            
                ##ll = getGeoloc(add).encode('ascii', 'ignore') ## 5625 Boul. M\xe9tropolitain St-L\xe9onard Quebec H1P 1X3  This may not be working
                ## dummy lat, lng = getGeoloc(add)
                
                lat = 99.99
                lng = 77.77
                
                print("lat and long are:", lat, " ", lng)
                
                OutLat = lat
                OutLng = lng
                
                pos = "pos"
            
                ## if counter == 2: ## This constraint needs to be removed for production!!! former position of if, will move it up
                ##print("DDDDDDDDDDDDDDDDDDD there are more than 2 view URLS then I break!!!")
                
                ## Getting Biz name and rating
                
                ##start = url.find("Canada/") + 7
                ##end = url.find('-store', start) ## needs to be between Canada/ and -store!!
                
                ##print "BEFORE parameters for calling google_places are lat, lng, pos =", lat, lng, pos 
                
                               
                OutName = "OutName"
                OutRtg = "5.0" ## needs to be str                  
                   
                OutTyp = "a, b, c, d"  ## needs to be str              
                
                    ## here I include the code to gather the columns we need to conform our table
                              
                    ## print for debugging!
                print("===============================")
                print "Name=", OutName 
                print "add=",  OutAdd
                print "City=", OutCity 
                print "Prov=", OutProv 
                print "Post=", OutPost 
                print "Lat=",  OutLat 
                print "Lng=",  OutLng  
                print "Rtg=",  OutRtg  
                print "Typ=",  OutTyp 
                print("===============================")
                
                with open('OUTPUT.csv', 'a') as csvfile:
                    fieldnames = ['Name', 'Address', "City", "Province", "Postal Code", "Latitude", "Longitude", "Rating", "Types"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    ###############################################################################################################################################################################################
                    writer.writerow({'Name': OutName, 'Address': OutAdd, "City": OutCity, "Province": OutProv, "Postal Code": OutPost, "Latitude": OutLat, "Longitude": OutLng, "Rating": OutRtg, "Types": OutTyp})
                    ###############################################################################################################################################################################################    
                
                    countw+=1
                    print("Im writing #", countw)
                 
                
    return


# Main()
# 
# 1 Read all categories found in the website "www.mystore411.com"
# 
# 1 Read the URL for each category found on 1. to get the list of businesses
# 
# 3 Read each of the Businesses and test if it has State (Province) locations
# 
# 4 If a Business has presence in Provinces, test if has presence in Cities
# 
# 5 Retrieve the business address and write it in the output file

# In[50]:


## main()

url = "https://mystore411.com"

lCat   = []
lBiz   = []
lSta   = []
lCit   = []
lABiz  = []
lASta  = [] 
lACit  = []

##f = open("./fscraper-OUTPUT", "w") ## ???


if os.path.exists("./OUTPUT.csv"):
  os.remove("./OUTPUT.csv")
  print "*** OUTPUT file DELETED ***"
else:
  print("The file does not exist")

with open('OUTPUT.csv', 'a') as csvfile:
    fieldnames = ['Name', 'Address', "City", "Province", "Postal Code", "Latitude", "Longitude", "Rating", "Types"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


print("top url is", url)

##store = urllib2.urlopen(url,context = context)
##from bs4 import BeautifulSoup
##soup = BeautifulSoup(store, "lxml")

##print ("Process of scrapping website STARTS at:", datetime.datetime.now())
##for a in soup.find_all('a',href=True): ## LOOK FOR ALL CATEGORIES  
##    lCat = getCategories(lCat)
    
##print("&&&&&&&&&&&&&& This is the list of categories:", lCat)

##for i in range(0, len(lCat)):
##for i in range(0, 3): ## delete for production 
##    lBiz = getBusinesses(lCat[i])
##    lABiz += lBiz
##print("&&&&&&&&&&&&&& This is the list of ALL Businesses in each category:", lABiz)

##print(" =============================== in getStates =======================================")

##for i in range(0, len(lABiz)):
##for i in range(0, 3):   ## delete for production 
##    lSta = getStates(lABiz[i])
##    lASta += lSta
##print("&&&&&&&&&&&&&& This is the list of ALL States in each business:", lASta)

## writing lASta into a file for debugging purposes!!!!
##f = open("./fscraper-lASta", "w")
##for i in range(0,len(lASta)):
##    f.write(lASta[i]+",")
##### not here!!! f.close()

##for i in range(0, len(lASta)):
##for i in range(0, 3):  ## delete for production  
##    lCit = getCities(lASta[i])
##    lACit += lCit
##    print("%%%%%%%% TGetlocation(lAsta[i]) %%%%%%%%%%%%%%%% i=", i, " ", lASta[i])
    ## Add this to V6!!
##    TGetLocation(lASta[i])


##print "#### writing lACit into a file for debugging purposes!!!!"
##f = open("./fscraper-lACit", "w")
##for i in range(0,len(lACit)):
##    f.write(lACit[i]+",")
print("WTH")
f = "./fscraper-lACit"
lACit = open(f).read().split(",")
print(len(lACit))

i=0
print("@@@@@ lACit len is", len(lACit))
##for i in range(0, len(lACit)): ## Here retrieve all stores that are present in cities
for i in range(0, len(lACit)): ## TEST from 100 to 1000 occurrence, changed back from 0!
    print("@@@@ I AM PROCESSING i=", i, "lACit=", lACit[i])
    TGetLocation(lACit[i]) 

## print("&&&&&&&&&&&& This is the list of Cities in each State:", lACit) too much display!!!

print ("Process of scrapping website ENDED at:", datetime.datetime.now())

##f.close()


# In[ ]:


########################## END OF MAIN CODE ###################################################
