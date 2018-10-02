
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
# This version is just to estimate the volume of the output!! also to generates the data in CSVs to upload to the db
# 

# In[19]:


# initializations

import urllib2
import urllib
import requests
import time
import sys
import datetime
import csv
import os
import re

from bs4 import BeautifulSoup


# In[20]:


from googleplaces import GooglePlaces, types, lang

MY_API_KEY = 'AIzaSyBCStYlYkMxdXJYJjuVEINvU7U8HBarCJ0' ## THIS IS MY OWN KEY

google_places = GooglePlaces(MY_API_KEY)


# In[21]:


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


# In[22]:


## these two lines to avoid the SSL error
import ssl
context = context = ssl._create_unverified_context()


# In[23]:


def getCategories(lCat):
    ## print("in getCategories OK file gen")
    ## print("inCategories href=", a['href'])
    global id 
    
    cid = ""
    cID = 0
    
    if "category" in a['href']:
        
        urlCID = "http://mystore411.com" + str(a['href'])
        
        ##print("a[href]=", a['href'])
        ##print("urlCID=", urlCID)
        
        start = urlCID.find("category/") + 9
        cid = urlCID[start:] 
        
        print ">>>>>>>>>>>>>>>>>>>> id:", id, "<<<<<"
        
        print "XXXXXXXXXXXXXXXXX type de id es:", type(id)
        
        id += 10
        
        iid = "%03d" % (id)

        print("$$$$$$$$$$$$$$$$$$ getCategory Found id is ", cid, " with id:", iid) 
        
        urlCID = urlCID + "/cid=" + str(iid)
        
        print("$$$$$$$$$$$$$$$$$$ This is the urlCID with id:", urlCID)
        
        lCat.append(urlCID)
        
        
        ## 
        ## lCid.append(cid)
        
        ## print("This is the dictionary of categories inside getCategories:", dCat)
        
          
    return lCat, id, cid


# In[24]:


## New getbiz
def getBizNew(url):
    print "##################### at getBizNew ######################"
    lBiz =[]
    bizID = ""
    bizDesc = ""
    
    from bs4 import BeautifulSoup
    
    end = url.find('/cid=', 0)
    newURL = url[0: end]
    
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$at getBizNew, I will read url=", newURL)
    store = urllib2.urlopen(newURL,context = context)   
    cat_soup = BeautifulSoup(store, "lxml") 
    
    start = url.find('/cid=') + 5 ## CAT_ID
    cid = url[start:]  
    
    print "########################### cid is:", cid ## for all biz under same category
    
    
    
    start = url.find('/cid=') + 5 ## CAT_ID
    cid = url[start:]  
    
    print "########################### cid is:", cid ## for all biz under same category
    
    BizList = str(cat_soup.find_all("a", href=True)).split(",")
    
    for i in range(0,len(BizList)):
        
        
        if re.search(r"/store/listing", BizList[i]):
            start = BizList[i].find('listing/') + 8
            end = BizList[i].find('\">')
            urlR = BizList[i][start:end]
            url = "https://www.mystore411.com/store/listing/" + urlR
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@ at getBizNew BizList url for i=", i," is:", url
            
            store = urllib2.urlopen(url,context = context)   
            store_soup = BeautifulSoup(store, "lxml") 
            
            StoreList = str(store_soup.find_all("a", href=True)).split(",")
            
            for j in range (0, len(StoreList)):
                ## print ("!!!!!!!!!!!!!!!!!!!!!!! THIS IS THE STORELIST[i] I AM GOING TO READ!!", StoreList[j])
                if re.search(r"/store/listing", StoreList[j]):
                    if re.search(r'/Canada/', StoreList[j]):
                        print("################ /Canada/ was found in StoreList[", j,"]=", StoreList[j])
                        ## hey StoreList doesnt have URLs!!!  
                
                        start = StoreList[j].find('listing/') + 8
                        end = StoreList[j].find('-store', start)
                        biz = StoreList[j][start:end]
                                
                        print("**** Biz=", biz)
            
                        url = "https://www.mystore411.com/store/listing/" + biz + "-store-locations" 
                
                        lBiz.append(url)
                    
                        ## print "&&&&& WTH lBiz is", lBiz
                    
                        start = url.find('store/listing/') + 14 ## BIZ_ID
                        end = url.find('/Canada/', start)
                        bizID = url[start:end]
            
                        print '#### bizID=', bizID
                        
                        start = url.find('/Canada/') + 8  ## BIZ_DESC
                        end = url.find('-store', start)
                        bizDesc = url[start:end]
            
                        print "#### bizDesc=", bizDesc
            
                        print "###################### WRITE RECORD BZC #########################"
                        iibizID  = "%05d" % (int(bizID))
                        with open('BZC.csv', 'a') as csvfile:
                            fieldnames = ['BIZ_ID', 'BIZ_DESC', 'CAT_ID']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            #####################################################################
                            writer.writerow({'BIZ_ID': iibizID, 'BIZ_DESC': bizDesc, 'CAT_ID':cid})  
                            #####################################################################
                        
                        ## print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& This is lBiz inside getNewBiz:", lBiz

    return lBiz
                    
                
        


# In[25]:


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


# In[26]:


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
    ##print "debugging span=", span
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
    
    return add, address, loc, reg, pos


# In[27]:


def getGeoloc(add):
    ##
    ## get coordinates of address
    
    param = {'address': add, 'key': 'AIzaSyBCStYlYkMxdXJYJjuVEINvU7U8HBarCJ0'} ## here used Google API
    geo_s = 'https://maps.googleapis.com/maps/api/geocode/json' ## needed
    
    response = requests.get(geo_s, params=param)

    json_dict = response.json()

    ## testing
    lat = json_dict['results'][0]['geometry']['location']['lat']
    lng = json_dict['results'][0]['geometry']['location']['lng']
    
    ##ll = str(lat) + "," + str(lng)
    
    time.sleep(2) 
    
    return str(lat), str(lng)


# In[28]:


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
        


# In[29]:


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

                    start = ProvList[i].find('list_state/') + 11 ## strings start in [0] in python!
                    end = ProvList[i].find('-store', start)
                    prov = ProvList[i][start:end]
            
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


# In[30]:



def TGetLocation(url):
    print("at TGetLocation with url:", url)    
    ##time.sleep(2) ####################### added to hopefully avoid program stops abruptly
    
    OutName = " "
    OutAdd  = " "
    OutCity = " "
    OutProv = " "
    OutPost = " "
    OutLat  = " "
    OutLng  = " "
    OutRtg  = " "
    OutTyp  = " "
    
    global countw
    
    ##try:
    time.sleep(5) ## introducing a delay to see if makes a difference! ## raised to 5 as per Winston
    f = urllib.urlopen(url, context=context)
    store = f.read()
    
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
            print("counter = ", counter)
            storeURL = ('https://mystore411.com' + a['href']).encode('utf-8') ## Here I conform the URL for reading the store name of the biz
            print("BEFORE ====== storeURL is:", storeURL, "a[href] is:", a['href'])
            if counter >= 1: ## delete for production!! just writing 1 for TESTING!!!! ##########################################
                
                storeURL = ('https://mystore411.com' + a['href']).encode('utf-8') ## Here I conform the URL for reading the store name of the biz
                print("at TGetLocation ====== storeURL is:", storeURL, "a[href] is:", a['href'])
                
                add, OutAdd, OutCity, OutProv, OutPost = getAddress(storeURL)
                
                print("*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&**&*&*&* OutProv=", OutProv)
                
                print("The address of the biz is:", OutAdd + " " + OutCity + " " + OutProv + " " + OutPost)
            
                ##ll = getGeoloc(add).encode('ascii', 'ignore') ## 5625 Boul. M\xe9tropolitain St-L\xe9onard Quebec H1P 1X3  This may not be working
                
                lat, lng = getGeoloc(add) ## Query Google API
                
                
                print("lat and long are:", lat, " ", lng)
                
                OutLat = lat
                OutLng = lng
                
                ##pos = "pos"
                
                ## Store ID
                start = storeURL.find('/view/') + 6
                end = storeURL.find('/Canada/')
                OutSid = storeURL[start:end]
                ## here you need to extract the bizname
                
                OutName = "OutName"
                ############ QUERY 2 Google API
                
                start = url.find("Canada/") + 7
                end = url.find('-store', start) ## needs to be between Canada/ and -store!!
                bizN = url[start:end]
                
                try:
                    query_result = google_places.nearby_search(lat_lng = {'lat': lat, 'lng': lng}, name = bizN) ## Need to get the store name!
                    print "AFTER parameters for calling google_places are lat, lng, pos =", lat, lng, bizN 
                    time.sleep(5) ## think a delay is necessary otherwise may crash!! ###########################################
                
                    place_id = query_result.places[0].place_id ## gets the place id 
                    print "place_id=", place_id 
                
                    ## gets rating given a place_id

                    store = google_places.get_place(place_id) ## gets the rating given the place id

                    print("Store rating of", str(store.name), "is=", store.rating)
                    ##time.sleep(2) ## think a delay is necessary otherwise may crash!! ###########################################
                
                    ## conform table (within scope of if for testing)
                
                    OutBN = str(store.name) 
                    OutRtg = str(store.rating) ## needs to be str
                    
                 
                    OutTyp = unlistTypes(store.types)  ## needs to be str  

                ############ END Google Query
                                
                    ## here I include the code to gather the columns we need to conform our table
                              
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
                
                    ## STORE_ID
                    start = storeURL.find('/view/') + 6
                    end = storeURL.find('/Canada/')
                    OutSid = storeURL[start:end]
                
                    ## STORE_NAME
                    start = storeURL.find('/Canada/') + 8
                
                    OutSna = storeURL[start:]   
                
                    ## STORE_NAME_API
                    ## need to query API
                    OutSnw = "GOOGLE API"
                
                    ##BIZ_ID
                    ## here I need to sequentially read BZC.csv and find the BIZ_ID
                    OutBid = 12345 ## str??
                                
                    ##PROV_ID
                
                    ##CITY_ID     
                
                    ## rest of fields already recovered
                
                    with open('SL.csv', 'a') as csvfile:
                        fieldnames = ['STORE_ID', 'STORE_NAME_WEB', 'STORE_NAME_API', 
                                      'BIZ_ID', 'PROV_ID', 'CITY_ID', 'ADDRESS', 
                                      'POSTAL_CODE', "LATITUDE", "LONGITUDE", 
                                      'RATING', 'TYPES']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        ##########################################################################################
                        writer.writerow({'STORE_ID': OutSid, 'STORE_NAME_WEB': OutSnw,"STORE_NAME_API": OutSna, 
                                         'BIZ_ID': OutBid, "PROV_ID": OutProv, 'CITY_ID':OutCity, 'ADDRESS':OutAdd,
                                         "POSTAL_CODE": OutPost, "LATITUDE": OutLat,"LONGITUDE": OutLng, 
                                         "RATING": OutRtg, "TYPES": OutTyp})
                        ##########################################################################################    
                
                        ##countw+=1
                        ##print("Im writing #", countw)              
                
                
                    with open('SAMPLE.csv', 'a') as csvfile:
                        fieldnames = ['Store_id', 'Store_Name', 'Biz_Name', 'Address', "City", 
                                      'Province', 'Postal Code','Latitude', 'Longitude', 'Rating', 'Types']

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        ##################################################################################
                        writer.writerow({'Store_id': OutSid, 'Store_Name':OutSna, 'Biz_Name': OutBN, 
                                         'Address': OutAdd, 'City': OutCity, 'Province': OutProv, 
                                         'Postal Code': OutPost, 'Latitude': OutLat, 'Longitude': OutLng, 
                                         'Rating': OutRtg, 'Types': OutTyp})
                        ##################################################################################    
                        print("Im writing #", countw)
                        countw+=1
                    
                        if countw >= 1000:
                            ## set to 10 just for testing!!
                            print("*********  EXECUTION OF PROGRAM TERMINATED ***********")
                            return 
                except:
                    print "********* ERROR when trying to get the place_id Google API didn't like it! **********"                   
    return


# In[31]:


def writeOutputfh():
    OUT = "./SAMPLE.csv"
    if os.path.exists(OUT):
        os.remove(OUT)
        print "***", OUT, " file DELETED ***"
    else:
        print("The file", OUT, " does not exist")

    with open(OUT, 'a') as csvfile:
        fieldnames = ['Store_id', 'Store_Name', 'Biz_Name', 'Address', "City", 
                      'Province', 'Postal Code','Latitude', 'Longitude', 'Rating', 'Types']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# In[32]:


def writeCidfh():
    CID = "./CID.csv"
    if os.path.exists(CID):
        os.remove(CID)
        print "*** ", CID, " file DELETED ***"
    else:
        print("The file ", CID, " does not exist")

    with open(CID, 'a') as csvfile:
        fieldnames = ['CAT_ID', 'CAT_DESC']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# In[33]:


def writeBizCfh():
    BZC = "./BZC.csv"
    if os.path.exists(BZC):
        os.remove(BZC)
        print "*** ", BZC, " file DELETED ***"
    else:
        print("The file", BZC, " does not exist")

    with open(BZC, 'a') as csvfile:
        fieldnames = ['BIZ_ID', 'BIZ_DESC', 'CAT_ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()   


# In[34]:


def writeStoLfh():
    SL = "./SL.csv"
    if os.path.exists(SL):
        os.remove(SL)
        print "*** ", SL, " file DELETED ***"
    else:
        print("The file", SL, " does not exist")

    with open(SL, 'a') as csvfile:
        fieldnames = ['STORE_ID', 'STORE_NAME_WEB', 
                      'STORE_NAME_API', 'BIZ_ID', 'PROV_ID', 
                      'CITY_ID', 'ADDRESS', 'POSTAL_CODE', 
                      "LATITUDE", "LONGITUDE", 'RATING', 'TYPES']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()   


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

# In[ ]:


## main()

url = "https://mystore411.com"

lCat   = []

id = 10

cid    = "" ## Category id only
lBiz   = []
lSta   = []
lCit   = []
lABiz  = []
lASta  = [] 
lACit  = []

##f = open("./fscraper-OUTPUT", "w") ## ???


writeOutputfh()
###############

print("top url is", url)
print ("Process of scraping website STARTS at:", datetime.datetime.now())

store = urllib2.urlopen(url,context = context)
from bs4 import BeautifulSoup
soup = BeautifulSoup(store, "lxml")

writeCidfh()
############
id = 0
for a in soup.find_all('a',href=True): ## LOOK FOR ALL CATEGORIES 
    
    lCat, x, cid = getCategories(lCat)
    print("############# id antes de +10:", id)
    

    x = int(x)
    x = "%03d" % (x)
    
    ###x = x + 10
    
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% x=", x, "=="
    
    ##cID = "%03d" % (id)
        
    print ("######### id after +10:", id)

    if cid:
  
        with open('CID.csv', 'a') as csvfile:
            fieldnames = ['CAT_ID', 'CAT_DESC']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            ###########################################################
            writer.writerow({'CAT_ID': x, 'CAT_DESC': cid})  
            ###########################################################  

writeBizCfh()
#############

## print("&&&&&&&&&&&&&& This is the list of categories:", lCat)
print("lABiz is", lABiz)
for i in range(0, len(lCat)):
    lBiz = getBizNew(lCat[i]) ## This f is not returning lBiz!!
    ##print "######################## This is the BIZ I will write:", lBiz ## too much output lBiz contains the list of biz or the cat, while lABiz contains all biz of all cat! 
    lABiz += lBiz


##print("&&&&&&&&&&&&&& This is the list of ALL Businesses in each category:", lABiz)


print(" =============================== in getStates =======================================")

for i in range(0, len(lABiz)): 
    print("Main ############# i=", i, "len(lABiz):", len(lABiz))
    lSta = getStates(lABiz[i])
    lASta += lSta
##print("&&&&&&&&&&&&&& This is the list of ALL States in each business:", lASta)

## writing lASta into a file for debugging purposes!!!!
f = open("./lASta2", "w")
for i in range(0,len(lASta)):
    f.write(lASta[i]+",")

writeStoLfh()
#############

for i in range(0, len(lASta)): 
    lCit = getCities(lASta[i])
    lACit += lCit
    TGetLocation(lASta[i])

##print "#### writing lACit into a file for debugging purposes!!!!"
f = open("./lACit2", "w")
for i in range(0,len(lACit)):
    f.write(lACit[i]+",")

###f = "./lACit"
###lACit = open(f).read().split(",")
###print(len(lACit))

i=0
## print("@@@@@ lACit len is", len(lACit))
for i in range(0, len(lACit)): ## Here retrieve all stores that are present in cities
###for i in range(0, len(lACit)): ## TEST from 100 to 1000 occurrence, changed back from 0!
###    print("@@@@ I AM PROCESSING i=", i, "lACit=", lACit[i])
    TGetLocation(lACit[i]) 

## print("&&&&&&&&&&&& This is the list of Cities in each State:", lACit) too much display!!!

print ("Process of scrapping website ENDED at:", datetime.datetime.now())


##f.close()


# In[ ]:


########################## END OF MAIN CODE ###################################################

