# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 14:47:20 2018

@author: jyiu04
"""

#Grab the necessary information for All schools in North York

#for all the comment field with notes - refer to test3_combined.py

############################
#   STEP 1 - SCHOOL NAME   #
############################

import urllib
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#need to loop through pages
req = Request('https://ca.ratemyteachers.com/ontario/north-york/1', headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage,'lxml')

#school name is stored under h3 tag
name_tag_all = soup.findAll('h3',attrs={'class': 'school_name'})

str_school_name = str(name_tag_all)
school_name = BeautifulSoup(str_school_name, "lxml").get_text()

school_name

type(school_name)

clean_school_name=re.sub('\'|\\n\n|\[|\]','',school_name)

type(clean_school_name)

clean_school_name

import re

test =[]

for container in name_tag_all:
    test1 = container.a.text
    test2=re.sub('\'|\\n','',test1)
    test.append(test2)    

test
type(test)
len(test)

clean_school_list = clean_school_name.split(",")

len(clean_school_list)


#################################
#   STEP 2 - INSTITUTION TYPE   #
#################################

#Institution type div class='institution_type'
institution_tag_all = soup.findAll('div',{'class': 'institution_type'})

str_institution_type = str(institution_tag_all)

institution_type = BeautifulSoup(str_institution_type, "lxml").get_text()

institution_type

clean_institution_type=re.sub('\'|\\n\n|\[|\]','',institution_type)

clean_institution_list = clean_institution_type.split(",")

len(clean_institution_list)
################################
#   STEP 3 - OVERALL RATINGS   #
################################

ratings_tag_trial = soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'})

clean_ratings_trial = []


for each_tag in ratings_tag_trial:
    clean_ratings_trial.append(each_tag["title"])

clean_ratings_trial

len(clean_ratings_trial)
#to remove the city rating and the last two rateit tag which doesn't contribute to any values
clean_ratings_all = clean_ratings_trial[1:-2]
clean_ratings_all
len(clean_ratings_all)
##############################
#   STEP 4 - TOTAL RATINGS   #
##############################

ratings_count_all = soup.findAll('div',{'class': 'rating_count'})

print(ratings_count_all)

str_ratings_count = str(ratings_count_all)

ratings_count = BeautifulSoup(str_ratings_count, "lxml").get_text()

ratings_count

clean_ratings_count=re.sub('\'|\\n|\[|\]','',ratings_count)

clean_ratings_count_1 = clean_ratings_count.replace('ratings','')

clean_ratings_count_final = clean_ratings_count_1.replace('rating','')

clean_ratings_count_list = clean_ratings_count_final.split(", ")


################################
#   STEP 5 - COMBINE RESULTS   #
################################

import pandas as pd

test_df = pd.DataFrame({'school': clean_school_list,
                        'institution': clean_institution_list,
                        'ratings': clean_ratings_all,
                        'Number_of_Reviews': clean_ratings_count_list})

print(test_df.info())

print(test_df)

test_df.to_csv("Output.csv")


########################################
#   STEP 6 - SIMPLIFY STEP 1-5 ABOVE   #
########################################

#import necessary libraries
import urllib
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

req = Request('https://ca.ratemyteachers.com/ontario/north-york/1', headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage,'lxml')

#List to store the scraped data in
school = []
institution = []
ratings = []
num_reviews = []
number_of_reviews = []

name_tag_all= soup.findAll('h3',class_= 'school_name')

    for container in name_tag_all:
        school_name = container.a.text.strip()
        school.append(school_name)    

    school

institution_tag_all = soup.findAll('div',{'class': 'institution_type'})

    for container in institution_tag_all:
        inst_name = container.text.strip()
        institution.append(inst_name)

    institution

rating_tag_all = soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'})

rating_tag_all[0]["title"]
    for container in rating_tag_all:
        if container["title"] != '':
            ratings.append(container["title"])

    ratings.remove(ratings[0])

    ratings

count_tag_all = soup.findAll('div',{'class': 'rating_count'})

    for container in count_tag_all:
        count = container.text.strip()
        num_reviews.append(count)            

    number_of_reviews_str = str(num_reviews).replace('\\nratings','')

    number_of_reviews1_str = number_of_reviews_str.replace('\\nrating','')

    number_of_reviews_list = number_of_reviews1_str.split(", ")

    #to remove the city rating and the last two rateit tag which doesn't contribute to any values
    number_of_reviews = number_of_reviews_list[1:-2]

    number_of_reviews

#get page number

#https://towardsdatascience.com/an-introduction-to-web-scraping-with-python-bc9563fe8860
    
######################################################
#   STEP 7 - lOOP THROUGH PAGES AND INCLUDE STEP 6   #
######################################################

import urllib
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas
import pdb #python debugging


#Base URL and get the last page in string
base_url = 'https://ca.ratemyteachers.com/ontario/north-york/'

r0 = Request(base_url, headers={'User-Agent':'Mozilla/5.0'})        
c0 = urlopen(r0).read()
soup0 = BeautifulSoup(c0,'lxml')
paging = soup0.find('li', attrs={'class':'last_page'})    
last_pg=paging.a['href'][-1]

#Empty lists to store the information we need
school = []
institution = []
#Ratings and Counts need manipulations after the for loop 
#since there are items sharing the same tag but need to be excluded
temp_ratings_lst=[]
temp_ratings_lst_mod=[]
ratings = []
temp_count_lst=[]
num_reviews = []
web_content_list=[]


#loop through pages
for page_number in range(1,int(last_pg)+1):
    url = base_url+str(page_number)
    r = Request(base_url+str(page_number),headers={'User-Agent':'Mozilla/5.0'})
    c = urlopen(r).read()
    soup = BeautifulSoup(c,'lxml')
 
    name_tag_all= soup.findAll('h3',class_= 'school_name') #25

    institution_tag_all = soup.findAll('div',{'class': 'institution_type'}) #25

    rating_tag_all = soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'})

    count_tag_all = soup.findAll('div',{'class': 'rating_count'})

   
    for container in name_tag_all:
        school_name = container.a.text.strip()
        school.append(school_name)    

    for container in institution_tag_all:
        inst_name = container.text.strip()
        institution.append(inst_name)
        
    for container in rating_tag_all:
        if container["title"] != '':
            temp_ratings_lst.append(container["title"])
    temp_ratings_lst_mod=temp_ratings_lst[1:]        
    temp_ratings_lst=[]
    #Extend needs to be used to append a list to another - append only works with single element
    ratings.extend(temp_ratings_lst_mod) #same indent level as for --> run after for loop
    
    for container in count_tag_all:
        num_reviews.append(container.text.strip().replace('\nratings','').replace('\nrating',''))

#Check length of each list
len(school)
len(institution)
len(ratings) 
len(num_reviews)

# To make a dataframe with the list        
test_df = pandas.DataFrame({'school': school,
                           'institution': institution,
                           'ratings': ratings,
                           'Number_of_Reviews': num_reviews})

#To check working directory
import os
cwd = os.getcwd()
cwd

os.chdir('C:\\Users\\jonyi\\OneDrive\\Documents\\Data Science Mentorship')

test_df.to_csv("north_york_df.csv",encoding='utf-8', index=False)


###############################################################
#   STEP 8 - SIMPLIFY FOR LOOPS BY USING LIST COMPREHENSION   #
###############################################################
#simplify the 4 lists within for loop

#school1 = [x.a.text.strip() for x in name_tag_all]
#school1

#institution1 = [x.text.strip() for x in institution_tag_all]
#institution1
        
#ratings1 = [x["title"] for x in rating_tag_all if x["title"]!=''][1:]
#ratings1

#count1 = [x.text.strip().replace('\nratings','').replace('\nrating','') for x in count_tag_all]
#count1

import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas
import re

#Base URL and get the last page in string
base_url = 'https://ca.ratemyteachers.com/ontario/north-york/'
r0 = Request(base_url, headers={'User-Agent':'Mozilla/5.0'})        
c0 = urlopen(r0).read()
soup0 = BeautifulSoup(c0,'lxml')
last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1]    

#Empty lists to store the information we need
#Ratings and Counts need manipulations after the for loop since there are items sharing the same tag but need to be excluded
school = []
institution = []
ratings = []
count = []
web_content_list=[]

#loop through pages
for page_number in range(1,int(last_pg)+1):
    url = base_url+str(page_number)
    r = Request(base_url+str(page_number),headers={'User-Agent':'Mozilla/5.0'})
    c = urlopen(r).read()
    soup = BeautifulSoup(c,'lxml')
 
    #.extend has to be in a separate line because the function extend is an in-place function, ie it will make the changes to the original list and return None
    school = school + [x.a.text.strip() for x in soup.findAll('h3',class_= 'school_name')]
    
    institution = institution + [x.text.strip() for x in soup.findAll('div',{'class': 'institution_type'})]
        
    ratings = ratings + [x["title"] for x in soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'}) if x["title"]!=''][1:]
    
    count = count + [x.text.strip().replace('\nratings','').replace('\nrating','') for x in soup.findAll('div',{'class': 'rating_count'})]
    


# Test the length of each list
len(count)
len(ratings)
len(institution)
len(school)


##############################################################################################
#   STEP 9 - CONVERT STEP 8 INTO FUNCTION THAT CAN BE CALLED WHEN SCRAPING MULTIPLE CITIES   #
##############################################################################################

import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas
import re
#from time import sleep
#from random import randint

#Function to do the following:
#1. Take city and province as input
#2. Replace whitespaces in inputs with hyphen
#3. Get last page of the link for the particular city and province from inputs
#4. Loop through each page of the particular city and province
#5. Return 6 lists (province, city, schools, types, ratings, counts)

#create a test function to convert province and city with hyphens and get the last page
#if only 1 page, the find('li') will be None
#write an if clause to say is not None, and convert city_name and province to no space
#Seems to work


def test( province, city_name):
  if ' ' in province:
    prov0 = province.replace(' ','-')
  else:
    prov0 = province

  if ' ' in city_name:
    city0 = city_name.replace(' ','-')
  else:
    city0 = city_name
  
  base_url="https://ca.ratemyteachers.com/" + str(prov0) + "/" + str(city0) + "/"
  r0 = Request(base_url, headers={'User-Agent':'Mozilla/5.0'})        
  c0 = urlopen(r0).read()
  soup0 = BeautifulSoup(c0,'lxml')

  #check last page  
  if soup0.find('li', attrs={'class':'last_page'}) is not None:
    last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1]    
  else:
    last_pg='1'
  
  #Create Empty Lists for results
  prov = []
  city = []
  school = []
  institution = []
  ratings = []
  count = []
  
  for page_number in range(1,int(last_pg)+1):
    url = base_url+str(page_number)
    r = Request(base_url+str(page_number),headers={'User-Agent':'Mozilla/5.0'})
    c = urlopen(r).read()
    soup = BeautifulSoup(c,'lxml')
 
    prov = prov + [prov0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
    city = city + [city0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
    #.extend has to be in a separate line because the function extend is an in-place function, ie it will make the changes to the original list and return None
    school = school + [x.a.text.strip() for x in soup.findAll('h3',class_= 'school_name')]
    
    institution = institution + [x.text.strip() for x in soup.findAll('div',{'class': 'institution_type'})]
        
    ratings = ratings + [x["title"] for x in soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'}) if x["title"]!=''][1:]
    
    count = count + [x.text.strip().replace('\nratings','').replace('\nrating','') for x in soup.findAll('div',{'class': 'rating_count'})]
 
  return prov, city, base_url, last_pg, school, institution, ratings, count;

#print(test("New Brunswick","Ste Anne De Madawaska"))
#print(test("ontario","north York"))
test1 = test("ontario","north york")

test_school_list = test1[1]

len(test_school_list)
test_school_list
 

# End Goal: Write 2 for loops to grab a list of province and every city within the province
# 1). Grab the list of province
# 2). Iterate to grab every city's name within 1 province
# 3). Combine 1 and 2
# 4). Combine 3 with the test function above

####
#1.#
####
prov_url = "https://ca.ratemyteachers.com/"
r1 = Request(prov_url, headers={'User-Agent': 'Mozilla/5.0'})
c1 = urlopen(r1).read()
soup_prov = BeautifulSoup(c1, "lxml")
prov_lst = [x.text.strip() for x in soup_prov.findAll('div', {'class': 'state'})]

#should show 13 provinces in Canada in list format
prov_lst

####
#2.#
####

#Get list of ALL cities from the site with /1 at the end after the province name
#without the 1 it only shows a subset of the cities

######################################################
#province needs to be replaced once combining 1 and 2#
######################################################
city_url = "https://ca.ratemyteachers.com/" + str('ontario') + '/' + '1'
r2 = Request(city_url, headers={'User-Agent': 'Mozilla/5.0'})
c2 = urlopen(r2).read()
soup_city = BeautifulSoup(c2,"lxml")

if len(soup_city.findAll('div', {'class': 'text'}))>1:
    last_pg_city = soup_city.findAll('div', {'class': 'text'})[1].text.strip()[-1]
else:
    last_pg_city = '1'

city_url_1 = "https://ca.ratemyteachers.com/" + str('ontario') + '/'

city_lst=[]

for page in range(1,int(last_pg_city)+1):
    url = city_url_1+str(page)
    r3 = Request(city_url_1+str(page),headers={'User-Agent':'Mozilla/5.0'})
    c3 = urlopen(r3).read()
    soup3 = BeautifulSoup(c3,"lxml")
    
    #get last page of each province for the list of cities
    city_lst = city_lst + [x.text.strip() for x in soup3.findAll('div', {'class': 'city'})]

len(city_lst)

city_lst



################################################################
# NEXT STEP: use nested for loops to get a list of provinces with their corresponding cities?
#            THEN APPLY the DEF?
#
# 20181127 - trial run

#20181129 - change request(url,xxxx) to requests.get(url etc)
#otherwise can't add timeout = 5 etc
#seems like we need to change ip, user agent etc

import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas
import re
from time import sleep
from random import randint
import requests
from lxml.html import fromstring
#from fake_useragent import UserAgent
import random

#def get_proxies():
#    url = 'https://free-proxy-list.net/'
#    response = requests.get(url)
#    parser = fromstring(response.text)
#    proxies = set()
#    for i in parser.xpath('//tbody/tr')[:10]:
#        if i.xpath('.//td[7][contains(text(),"yes")]'):
#            #Grabbing IP and corresponding PORT
#            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#            proxies.add(proxy)
#    return proxies
#proxies_lst = get_proxies()
#print(proxies_lst)
#type(proxies_lst)


proxies_req = requests.get('https://www.sslproxies.org/',headers={'User-Agent':'Mozilla/5.0'})
proxies_doc = proxies_req.content
soup_prox = BeautifulSoup(proxies_doc, 'lxml')
proxies_table = soup_prox.find(id='proxylisttable')

proxies_rand=[]

# Save proxies in the array
for row in proxies_table.tbody.find_all('tr'):
    proxies_rand.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
                    })

def random_proxy():
  return random.randint(0, len(proxies_rand) - 1)
    
# Choose a random proxy
proxy_index = random_proxy()
proxy = proxies_rand[proxy_index]
proxy['ip']
print(proxy)

proxies_rand

#from itertools import cycle
#import traceback
#proxy_pool = cycle(proxies_lst)

user_agent_list=[
        #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

#Function to do the following:
#1. Take city and province as input
#2. Replace whitespaces in inputs with hyphen
#3. Get last page of the link for the particular city and province from inputs
#4. Loop through each page of the particular city and province
#5. Return 6 lists (province, city, schools, types, ratings, counts)

#create a test function to convert province and city with hyphens and get the last page
#if only 1 page, the find('li') will be None
#write an if clause to say is not None, and convert city_name and province to no space
#Seems to work

#test_url="https://ca.ratemyteachers.com/" + "ontario" + "/" + "north-york" + "/1"
#r_test = requests.get(test_url, timeout=5, headers={'User-Agent':'Mozilla/5.0'})        
#c_test = r_test.content
#soup_test = BeautifulSoup(c_test,'lxml')
#r_test.status_code




#add proxies
#proxies = {'http' : 'http://10.10.0.0:0000',  
#          'https': 'http://120.10.0.0:0000'}
#page_response = requests.get(page_link, proxies=proxies, timeout=5)  


#test randomizing user agent and proxies
#user_agent_list = [
#   #Chrome
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
#    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#    #Firefox
#    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
#    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
#    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
#    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
#    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
#    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
#    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
#    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
#    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
#    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
#    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
#    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
#    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
#]

#len(user_agent_list)
#user_agent = random.choice(user_agent_list)
#url = 'https://httpbin.org/user-agent'

#for i in range(1, 6):
#    user_agent = random.choice(user_agent_list)
#    #Set the headers 
#    headers = {'User-Agent': user_agent}
#    #Make the request
#    response = requests.get(url,headers=headers)
    
#    print("Request #%d\nUser-Agent Sent:%s\nUser Agent Recevied by HTTPBin:"%(i,user_agent))
#    print(response.content)
#    print("-------------------\n\n")


def test( province, city_name):
    if ' ' in province:
        prov0 = province.replace(' ','-')
    else:
        prov0 = province
    if ' ' in city_name:
        city0 = city_name.replace(' ','-')
    else:
        city0 = city_name
    user_agent = random.choice(user_agent_list)
    headers= {'User-Agent': user_agent}
    proxy_index = random_proxy()
    proxy = proxies_rand[proxy_index]
    proxies = "https://"+str(proxy['ip'])+":"+str(proxy['port'])
    #prox= random.choice(proxies_lst)
    #proxies = prox
    base_url="https://ca.ratemyteachers.com/" + str(prov0) + "/" + str(city0) + "/"
    prov=[]
    city=[]
    school=[]
    institution=[]
    ratings=[]
    count=[]
    try:
        r0 = requests.get(base_url, proxies={"https":proxies}, timeout=5, headers=headers)
        c0=r0.content
        soup0 = BeautifulSoup(c0,'lxml')
        if soup0.find('li', attrs={'class':'last_page'}) is not None:
            last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1] 
        else:
            last_pg='1'
        for page_number in range(1,int(last_pg)+1):
            url = base_url+str(page_number)
            r = requests.get(base_url+str(page_number), proxies={"https":proxies}, timeout=5, headers=headers)
            c=r.content
            soup = BeautifulSoup(c,'lxml')
            prov = prov + [prov0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
            city = city + [city0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
            school = school + [x.a.text.strip() for x in soup.findAll('h3',class_= 'school_name')]
            institution = institution + [x.text.strip() for x in soup.findAll('div',{'class': 'institution_type'})]
            ratings = ratings + [x["title"] for x in soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'}) if x["title"]!=''][1:]
            count = count + [x.text.strip().replace('\nratings','').replace('\nrating','') for x in soup.findAll('div',{'class': 'rating_count'})]
    except:
        del proxies_rand[proxy_index]
        print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
        proxy_index = random_proxy()
        proxy = proxies_rand[proxy_index]
    
    return prov, city, school, institution, ratings, count;

prov_url = "https://ca.ratemyteachers.com/"
r1 = requests.get(prov_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
c1=r1.content
soup_prov = BeautifulSoup(c1, "lxml")
prov_lst = [x.text.strip() for x in soup_prov.findAll('div', {'class': 'state'})]


#should show 13 provinces in Canada in list format
prov_lst


full_prov_lst = []
city_lst = []
        

for prov in prov_lst:
    #Get the number of pages of cities for each province
    city_url = "https://ca.ratemyteachers.com/" + str(prov.replace(' ','-')) + '/' + '1'
    r2 = requests.get(city_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
    c2 = r2.content
    soup_city = BeautifulSoup(c2,"lxml")

    if len(soup_city.findAll('div', {'class': 'text'}))>1:
        last_pg_city = soup_city.findAll('div', {'class': 'text'})[1].text.strip()[-1]
    else:
        last_pg_city = '1'

    city_url_1 = "https://ca.ratemyteachers.com/" + str(prov.replace(' ','-')) + '/'

    for page in range(1,int(last_pg_city)+1):
        url = city_url_1+str(page)
        r3 = requests.get(city_url_1+str(page), timeout=5, headers={'User-Agent':'Mozilla/5.0'})
        c3 = r3.content
        soup3 = BeautifulSoup(c3,"lxml")
    
        #get last page of each province for the list of cities
        full_prov_lst = full_prov_lst + [prov for x in range(0,len(soup3.findAll('div', {'class': 'city'})))]
        city_lst = city_lst + [x.text.strip() for x in soup3.findAll('div', {'class': 'city'})]
        
        #Not Working!!
        # CURRENT PROBLEM! Province 13 , city -26xx instead of different numbers per province
        # cant assign the test function from above yet...
        #for x in soup3.findAll('div', {'class': 'city'}):
            #test(prov, x.text.strip())

full_prov_lst        
len(full_prov_lst)
 
city_lst
len(city_lst)

proxy
#check proxies and random user agent
test(full_prov_lst[1], city_lst[1])

#start running at 01:40am @ 20181205
for x in range(0, len(city_lst)):
    final_list = final_list + list(test(full_prov_lst[x], city_lst[x]))
    sleep(randint(2,7))
# Update: problem with the test function is it created a tuple which can not be "modified"
# Try: adding List(xxxxxx,xxx,xx,x,xx) after return to turn the output into a list
# THEN try zip to combined them together
#sample code: [item for items in zip(date_list, num_list_1, num_list_2) for item in items]
    
proxy 85.187.17.39:53281 deleted - 2:27am 57th proxy being deleted

#error again...proxies depleted
#check the last 6 element of final list and see which province/city has been run
#before it errored out
#take screenshot of error message too!!!!!    
    
len(final_list) #19314
final_list

#how to zip them and then flatten 
#matplotlib.cbook.flatten() will work for nested lists even if they nest more deeply than the example.
'''
import matplotlib
l = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]
print(list(matplotlib.cbook.flatten(l)))
l2 = [[1, 2, 3], [4, 5, 6], [7], [8, [9, 10, [11, 12, [13]]]]]
print list(matplotlib.cbook.flatten(l2))
'''

'''
for prov in prov_lst:
    for city in city_lst:
        test_final = test(prov, city)
'''

#####################################################################################################
#20181206 update:
#try not to use proxies and run the for loop three times instead
#flat_list = [item for sublist in l for item in sublist]

import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas
import re
from time import sleep
from random import randint
import requests
from lxml.html import fromstring
#from fake_useragent import UserAgent
import random


user_agent_list=[
        #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

#Function to do the following:
#1. Take city and province as input
#2. Replace whitespaces in inputs with hyphen
#3. Get last page of the link for the particular city and province from inputs
#4. Loop through each page of the particular city and province
#5. Return 6 lists (province, city, schools, types, ratings, counts)

#create a test function to convert province and city with hyphens and get the last page
#if only 1 page, the find('li') will be None
#write an if clause to say is not None, and convert city_name and province to no space
#Seems to work

#test_url="https://ca.ratemyteachers.com/" + "ontario" + "/" + "north-york" + "/1"
#r_test = requests.get(test_url, timeout=5, headers={'User-Agent':'Mozilla/5.0'})        
#c_test = r_test.content
#soup_test = BeautifulSoup(c_test,'lxml')
#r_test.status_code

def scrape( province, city_name):
    if ' ' in province:
        prov0 = province.replace(' ','-')
    else:
        prov0 = province
    if ' ' in city_name:
        city0 = city_name.replace(' ','-')
    else:
        city0 = city_name
    
    prov=[]
    city=[]
    school=[]
    institution=[]
    ratings=[]
    count=[]
        
    user_agent = random.choice(user_agent_list)
    headers= {'User-Agent': user_agent}
    base_url="https://ca.ratemyteachers.com/" + str(prov0) + "/" + str(city0) + "/"
    r0 = requests.get(base_url, timeout=5, headers=headers)
    c0=r0.content
    soup0 = BeautifulSoup(c0,'lxml')
    
    if soup0.find('li', attrs={'class':'last_page'}) is not None:
        last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1] 
    else:
        last_pg='1'

    for page_number in range(1,int(last_pg)+1):
        url = base_url+str(page_number)
        r = requests.get(base_url+str(page_number), timeout=5, headers=headers)
        c=r.content
        soup = BeautifulSoup(c,'lxml')

        prov = prov + [prov0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
        city = city + [city0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
        school = school + [x.a.text.strip() for x in soup.findAll('h3',class_= 'school_name')]
        institution = institution + [x.text.strip() for x in soup.findAll('div',{'class': 'institution_type'})]
        ratings = ratings + [x["title"] for x in soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'}) if x["title"]!=''][1:]
        count = count + [x.text.strip().replace('\nratings','').replace('\nrating','') for x in soup.findAll('div',{'class': 'rating_count'})]

    return prov, city, school, institution, ratings, count;

prov_url = "https://ca.ratemyteachers.com/"
r1 = requests.get(prov_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
c1=r1.content
soup_prov = BeautifulSoup(c1, "lxml")
prov_lst = [x.text.strip() for x in soup_prov.findAll('div', {'class': 'state'})]

#should show 13 provinces in Canada in list format
prov_lst

full_prov_lst = []
city_lst = []
    
for prov in prov_lst:
    #Get the number of pages of cities for each province
    city_url = "https://ca.ratemyteachers.com/" + str(prov.replace(' ','-')) + '/' + '1'
    r2 = requests.get(city_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
    c2 = r2.content
    soup_city = BeautifulSoup(c2,"lxml")

    if len(soup_city.findAll('div', {'class': 'text'}))>1:
        last_pg_city = soup_city.findAll('div', {'class': 'text'})[1].text.strip()[-1]
    else:
        last_pg_city = '1'

    city_url_1 = "https://ca.ratemyteachers.com/" + str(prov.replace(' ','-')) + '/'

    for page in range(1,int(last_pg_city)+1):
        url = city_url_1+str(page)
        r3 = requests.get(city_url_1+str(page), timeout=5, headers={'User-Agent':'Mozilla/5.0'})
        c3 = r3.content
        soup3 = BeautifulSoup(c3,"lxml")
        #get last page of each province for the list of cities
        full_prov_lst = full_prov_lst + [prov for x in range(0,len(soup3.findAll('div', {'class': 'city'})))]
        city_lst = city_lst + [x.text.strip() for x in soup3.findAll('div', {'class': 'city'})]
                
full_prov_lst        
len(full_prov_lst)
 
city_lst
len(city_lst)

scrape(full_prov_lst[0], city_lst[0])

#start running at 12:48am @ 20181207
final_list_1=[]
final_list_2=[]
final_list_3=[]

for x in range(0, 1000):
    final_list_1 = final_list_1 + list(scrape(full_prov_lst[x], city_lst[x]))
    sleep(randint(1,5))
    
for y in range(1000,2000):
    final_list_2 = final_list_2 + list(scrape(full_prov_lst[y], city_lst[y]))
    sleep(randint(2,4))

for z in range(2000,len(full_prov_lst)):
    final_list_3 = final_list_3 + list(scrape(full_prov_lst[z],city_lst[z]))
    sleep(randint(1,4))

len(final_list_1)
len(final_list_2)
len(final_list_3)


final_list_1_before = final_list_1
final_list_2_before = final_list_2
final_list_3_before = final_list_3

len(final_list_1_before)
len(final_list_2_before)
len(final_list_3_before)

'''
final_list_2[0:12]
final_list_3[1:12]
final_list_1[0:12]


final_list_2[0]
final_list_2[1]
final_list_2[2]
final_list_2[3]
final_list_2[4]
final_list_2[5]


city_lst[1000]


final_list_2a = scrape(full_prov_lst[1000], city_lst[1000])

final_list_2a

len(final_list_2a)

final_list_2b = scrape(full_prov_lst[1000], city_lst[1000])+scrape(full_prov_lst[1001], city_lst[1001])

final_list_2b
'''


#update: if no school for that city, prov and city returns nothing
# try modify scrape function and return city and province if no school
# then need to somehow chop the list into 6 columns
import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas
import re
from time import sleep
from random import randint
import requests
from lxml.html import fromstring
#from fake_useragent import UserAgent
import random


user_agent_list=[
        #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

#Function to do the following:
#1. Take city and province as input
#2. Replace whitespaces in inputs with hyphen
#3. Get last page of the link for the particular city and province from inputs
#4. Loop through each page of the particular city and province
#5. Return 6 lists (province, city, schools, types, ratings, counts)

#create a test function to convert province and city with hyphens and get the last page
#if only 1 page, the find('li') will be None
#write an if clause to say is not None, and convert city_name and province to no space
#Seems to work

#test_url="https://ca.ratemyteachers.com/" + "ontario" + "/" + "north-york" + "/1"
#r_test = requests.get(test_url, timeout=5, headers={'User-Agent':'Mozilla/5.0'})        
#c_test = r_test.content
#soup_test = BeautifulSoup(c_test,'lxml')
#r_test.status_code

def scrape( province, city_name):
    if ' ' in province:
        prov0 = province.replace(' ','-') 
    else:
        prov0 = province
    
    if ". " in city_name:
        city0 = city_name.replace(". ","-")
    elif "'" in city_name:
        city0 = city_name.replace("'","-")
    elif " " in city_name:
        city0 = city_name.replace(" ","-")
    else:
        city0 = city_name
    
    prov=[]
    city=[]
    school=[]
    institution=[]
    ratings=[]
    count=[]
        
    user_agent = random.choice(user_agent_list)
    headers= {'User-Agent': user_agent}
    base_url="https://ca.ratemyteachers.com/" + str(prov0) + "/" + str(city0) + "/"
    r0 = requests.get(base_url, timeout=5, headers=headers)
    c0=r0.content
    soup0 = BeautifulSoup(c0,'lxml')
    
    if soup0.find('li', attrs={'class':'last_page'}) is not None:
        last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1] 
    else:
        last_pg='1'

    for page_number in range(1,int(last_pg)+1):
        url = base_url+str(page_number)
        r = requests.get(base_url+str(page_number), timeout=5, headers=headers)
        c=r.content
        soup = BeautifulSoup(c,'lxml')

        if soup.findAll('h3',class_= 'school_name') == []:
            prov = province
        else:
            prov = prov + [province for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
        
        if soup.findAll('h3',class_= 'school_name') == []:
            city = city_name
        else:
            city = city + [city_name for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
        
        if soup.findAll('h3',class_= 'school_name') == []:
            school = "N/A"
        else:
            school = school + [x.a.text.strip() for x in soup.findAll('h3',class_= 'school_name')]
        
        if soup.findAll('h3',class_= 'school_name') == []:
            institution = "N/A"
        else:
            institution = institution + [x.text.strip() for x in soup.findAll('div',{'class': 'institution_type'})]
        
        if soup.findAll('h3',class_= 'school_name') == []:
            ratings = "N/A"
        else:
            ratings = ratings + [x["title"] for x in soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'}) if x["title"]!=''][1:]
        
        if soup.findAll('h3',class_= 'school_name') == []:
            count = "N/A"
        else:
            count = count + [x.text.strip().replace('\nratings','').replace('\nrating','') for x in soup.findAll('div',{'class': 'rating_count'})]

    return prov, city, school, institution, ratings, count;

prov_url = "https://ca.ratemyteachers.com/"
r1 = requests.get(prov_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
c1=r1.content
soup_prov = BeautifulSoup(c1, "lxml")
prov_lst = [x.text.strip() for x in soup_prov.findAll('div', {'class': 'state'})]

#should show 13 provinces in Canada in list format
prov_lst

full_prov_lst = []
city_lst = []
    
for prov in prov_lst:
    #Get the number of pages of cities for each province
    city_url = "https://ca.ratemyteachers.com/" + str(prov.replace(' ','-')) + '/' + '1'
    r2 = requests.get(city_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
    c2 = r2.content
    soup_city = BeautifulSoup(c2,"lxml")

    if len(soup_city.findAll('div', {'class': 'text'}))>1:
        last_pg_city = soup_city.findAll('div', {'class': 'text'})[1].text.strip()[-1]
    else:
        last_pg_city = '1'

    city_url_1 = "https://ca.ratemyteachers.com/" + str(prov.replace(' ','-')) + '/'

    for page in range(1,int(last_pg_city)+1):
        url = city_url_1+str(page)
        r3 = requests.get(city_url_1+str(page), timeout=5, headers={'User-Agent':'Mozilla/5.0'})
        c3 = r3.content
        soup3 = BeautifulSoup(c3,"lxml")
        #get last page of each province for the list of cities
        full_prov_lst = full_prov_lst + [prov for x in range(0,len(soup3.findAll('div', {'class': 'city'})))]
        city_lst = city_lst + [x.text.strip() for x in soup3.findAll('div', {'class': 'city'})]


final_list_1=[]
final_list_2=[]
final_list_3=[]
final_list_4=[]
final_list_5=[]
final_list_6=[]
final_list_7=[]

for a in range(0, 1000):
    final_list_1 = final_list_1 + list(scrape(full_prov_lst[a], city_lst[a]))
    sleep(randint(1,5))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_1)    

final_lst_11 = final_list_1[0::6]
final_lst_12 = final_list_1[1::6]
final_lst_13 = final_list_1[2::6]
final_lst_14 = final_list_1[3::6]
final_lst_15 = final_list_1[4::6]
final_lst_16 = final_list_1[5::6]    

import matplotlib
flat_final_11 = list(matplotlib.cbook.flatten(final_lst_11))
flat_final_12 = list(matplotlib.cbook.flatten(final_lst_12))
flat_final_13 = list(matplotlib.cbook.flatten(final_lst_13))
flat_final_14 = list(matplotlib.cbook.flatten(final_lst_14))
flat_final_15 = list(matplotlib.cbook.flatten(final_lst_15))
flat_final_16 = list(matplotlib.cbook.flatten(final_lst_16))

len(flat_final_11)
len(flat_final_12)
len(flat_final_13)
len(flat_final_14)
len(flat_final_15)
len(flat_final_16)

    
for b in range(1000,1100):
    final_list_2 = final_list_2 + list(scrape(full_prov_lst[b], city_lst[b]))
    sleep(randint(2,4))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_2)    

final_lst_21 = final_list_2[0::6]
final_lst_22 = final_list_2[1::6]
final_lst_23 = final_list_2[2::6]
final_lst_24 = final_list_2[3::6]
final_lst_25 = final_list_2[4::6]
final_lst_26 = final_list_2[5::6]    

flat_final_21 = list(matplotlib.cbook.flatten(final_lst_21))
flat_final_22 = list(matplotlib.cbook.flatten(final_lst_22))
flat_final_23 = list(matplotlib.cbook.flatten(final_lst_23))
flat_final_24 = list(matplotlib.cbook.flatten(final_lst_24))
flat_final_25 = list(matplotlib.cbook.flatten(final_lst_25))
flat_final_26 = list(matplotlib.cbook.flatten(final_lst_26))

len(flat_final_21)
len(flat_final_22)
len(flat_final_23)
len(flat_final_24)
len(flat_final_25)
len(flat_final_26)


for c in range(1100,1400):
    final_list_3 = final_list_3 + list(scrape(full_prov_lst[c], city_lst[c]))
    sleep(randint(2,4))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_3)    

final_lst_31 = final_list_3[0::6]
final_lst_32 = final_list_3[1::6]
final_lst_33 = final_list_3[2::6]
final_lst_34 = final_list_3[3::6]
final_lst_35 = final_list_3[4::6]
final_lst_36 = final_list_3[5::6]    

flat_final_31 = list(matplotlib.cbook.flatten(final_lst_31))
flat_final_32 = list(matplotlib.cbook.flatten(final_lst_32))
flat_final_33 = list(matplotlib.cbook.flatten(final_lst_33))
flat_final_34 = list(matplotlib.cbook.flatten(final_lst_34))
flat_final_35 = list(matplotlib.cbook.flatten(final_lst_35))
flat_final_36 = list(matplotlib.cbook.flatten(final_lst_36))

len(flat_final_31)
len(flat_final_32)
len(flat_final_33)
len(flat_final_34)
len(flat_final_35)
len(flat_final_36)


for d in range(1400,1700):
    final_list_4 = final_list_4 + list(scrape(full_prov_lst[d], city_lst[d]))
    sleep(randint(1,5))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_4)    

final_lst_41 = final_list_4[0::6]
final_lst_42 = final_list_4[1::6]
final_lst_43 = final_list_4[2::6]
final_lst_44 = final_list_4[3::6]
final_lst_45 = final_list_4[4::6]
final_lst_46 = final_list_4[5::6]    

flat_final_41 = list(matplotlib.cbook.flatten(final_lst_41))
flat_final_42 = list(matplotlib.cbook.flatten(final_lst_42))
flat_final_43 = list(matplotlib.cbook.flatten(final_lst_43))
flat_final_44 = list(matplotlib.cbook.flatten(final_lst_44))
flat_final_45 = list(matplotlib.cbook.flatten(final_lst_45))
flat_final_46 = list(matplotlib.cbook.flatten(final_lst_46))

len(flat_final_41)
len(flat_final_42)
len(flat_final_43)
len(flat_final_44)
len(flat_final_45)
len(flat_final_46)

final_list_5=[]

for e in range(1700,1900):
    final_list_5 = final_list_5 + list(scrape(full_prov_lst[e], city_lst[e]))
    sleep(randint(1,4))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_5)    

final_lst_51 = final_list_5[0::6]
final_lst_52 = final_list_5[1::6]
final_lst_53 = final_list_5[2::6]
final_lst_54 = final_list_5[3::6]
final_lst_55 = final_list_5[4::6]
final_lst_56 = final_list_5[5::6]    

flat_final_51 = list(matplotlib.cbook.flatten(final_lst_51))
flat_final_52 = list(matplotlib.cbook.flatten(final_lst_52))
flat_final_53 = list(matplotlib.cbook.flatten(final_lst_53))
flat_final_54 = list(matplotlib.cbook.flatten(final_lst_54))
flat_final_55 = list(matplotlib.cbook.flatten(final_lst_55))
flat_final_56 = list(matplotlib.cbook.flatten(final_lst_56))

len(flat_final_51)
len(flat_final_52)
len(flat_final_53)
len(flat_final_54)
len(flat_final_55)
len(flat_final_56)

final_list_6=[]

for f in range(1900,2300):
    final_list_6 = final_list_6 + list(scrape(full_prov_lst[f], city_lst[f]))
    sleep(randint(1,5))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_6)    

final_lst_61 = final_list_6[0::6]
final_lst_62 = final_list_6[1::6]
final_lst_63 = final_list_6[2::6]
final_lst_64 = final_list_6[3::6]
final_lst_65 = final_list_6[4::6]
final_lst_66 = final_list_6[5::6]    

flat_final_61 = list(matplotlib.cbook.flatten(final_lst_61))
flat_final_62 = list(matplotlib.cbook.flatten(final_lst_62))
flat_final_63 = list(matplotlib.cbook.flatten(final_lst_63))
flat_final_64 = list(matplotlib.cbook.flatten(final_lst_64))
flat_final_65 = list(matplotlib.cbook.flatten(final_lst_65))
flat_final_66 = list(matplotlib.cbook.flatten(final_lst_66))

len(flat_final_61)
len(flat_final_62)
len(flat_final_63)
len(flat_final_64)
len(flat_final_65)
len(flat_final_66)


final_list_7=[]

for g in range(2300,len(full_prov_lst)):
    final_list_7 = final_list_7 + list(scrape(full_prov_lst[g],city_lst[g]))
    sleep(randint(1,4))

#CHECK EACH LIST AND SEE IF THE LENGTH ARE CONSISTENT    
len(final_list_7)    

final_lst_71 = final_list_7[0::6]
final_lst_72 = final_list_7[1::6]
final_lst_73 = final_list_7[2::6]
final_lst_74 = final_list_7[3::6]
final_lst_75 = final_list_7[4::6]
final_lst_76 = final_list_7[5::6]    

flat_final_71 = list(matplotlib.cbook.flatten(final_lst_71))
flat_final_72 = list(matplotlib.cbook.flatten(final_lst_72))
flat_final_73 = list(matplotlib.cbook.flatten(final_lst_73))
flat_final_74 = list(matplotlib.cbook.flatten(final_lst_74))
flat_final_75 = list(matplotlib.cbook.flatten(final_lst_75))
flat_final_76 = list(matplotlib.cbook.flatten(final_lst_76))

len(flat_final_71)
len(flat_final_72)
len(flat_final_73)
len(flat_final_74)
len(flat_final_75)
len(flat_final_76)

final_lst_prov=[]
final_lst_city=[]
final_lst_school=[]
final_lst_inst=[]
final_lst_ratings=[]
final_lst_count=[]


final_lst_prov = flat_final_11 + flat_final_21 + flat_final_31 + flat_final_41 + flat_final_51 + flat_final_61 + flat_final_71
final_lst_city = flat_final_12 + flat_final_22 + flat_final_32 + flat_final_42 + flat_final_52 + flat_final_62 + flat_final_72
final_lst_school = flat_final_13 + flat_final_23 + flat_final_33 + flat_final_43 + flat_final_53 + flat_final_63 + flat_final_73
final_lst_inst = flat_final_14 + flat_final_24 + flat_final_34 + flat_final_44 + flat_final_54 + flat_final_64 + flat_final_74
final_lst_ratings = flat_final_15 + flat_final_25 + flat_final_35 + flat_final_45 + flat_final_55 + flat_final_65 + flat_final_75
final_lst_count = flat_final_16 + flat_final_26 + flat_final_36 + flat_final_46 + flat_final_56 + flat_final_66 + flat_final_76    

len(final_lst_prov)
len(final_lst_city)
len(final_lst_school)
len(final_lst_inst)
len(final_lst_ratings)
len(final_lst_count)

#To check working directory
import os
cwd = os.getcwd()
cwd

os.chdir('C:\\Users\\jonyi\\OneDrive\\Documents\\Data Science Mentorship')

final_school_df = pandas.DataFrame({'Province': final_lst_prov,
                                    'City': final_lst_city,
                                    'School': final_lst_school,
                                    'Institution': final_lst_inst,
                                    'Ratings': final_lst_ratings,
                                    'Number_of_Reviews': final_lst_count})

final_school_df.to_csv("final_school_df.csv",encoding='utf-8', index=False)


