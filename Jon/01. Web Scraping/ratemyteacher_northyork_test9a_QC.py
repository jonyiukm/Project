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

test_url="https://ca.ratemyteachers.com/" + "ontario" + "/" + "north-york" + "/1"
r_test = requests.get(test_url, timeout=5, headers={'User-Agent':'Mozilla/5.0'})        
c_test = r_test.content
soup_test = BeautifulSoup(c_test,'lxml')
r_test.status_code




#add proxies
proxies = {'http' : 'http://10.10.0.0:0000',  
          'https': 'http://120.10.0.0:0000'}
page_response = requests.get(page_link, proxies=proxies, timeout=5)  


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
  r0 = requests.get(base_url, timeout=5, headers={'User-Agent':'Mozilla/5.0'})        
  c0 = r0.content
  #sleep(randint(8,16))
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
    r = requests.get(base_url+str(page_number), timeout=5, headers={'User-Agent':'Mozilla/5.0'})
    c = r.content
    #sleep(randint(1,3))
    soup = BeautifulSoup(c,'lxml')
 
    prov = prov + [prov0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
    city = city + [city0 for x in range(0,len(soup.findAll('h3',class_= 'school_name')))]
    #.extend has to be in a separate line because the function extend is an in-place function, ie it will make the changes to the original list and return None
    school = school + [x.a.text.strip() for x in soup.findAll('h3',class_= 'school_name')]
    
    institution = institution + [x.text.strip() for x in soup.findAll('div',{'class': 'institution_type'})]
        
    ratings = ratings + [x["title"] for x in soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'}) if x["title"]!=''][1:]
    
    count = count + [x.text.strip().replace('\nratings','').replace('\nrating','') for x in soup.findAll('div',{'class': 'rating_count'})]
 
  return prov, city, school, institution, ratings, count;

prov_url = "https://ca.ratemyteachers.com/"
r1 = requests.get(prov_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
c1 = r1.content
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



#start running at 02:00am @ 20181129
for x in range(0, len(city_lst)):
    final_list = final_list + test(full_prov_lst[x], city_lst[x])
    

len(final_list)

    
    
#for prov in prov_lst:
#    for city in city_lst:
#        test_final = test(prov, city)



#####################################################################################################
base_home_page="https://ca.ratemyteachers.com/ontario" 
r1 = Request(base_url, headers={'User-Agent':'Mozilla/5.0'})        
c1 = urlopen(r1).read()
soup1 = BeautifulSoup(c1,'lxml')

  #check last page  
  if soup0.find('li', attrs={'class':'last_page'}) is not None:
    last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1]    
  else:
    last_pg='1'
  


##########################################################################################
#   STEP 10 - Setup time interval for scraping the data to prevent crashing the server   #
##########################################################################################

##################################################
# TESTING FROM WEB TUTORIALS                     #
#def sum( arg1, arg2 ):
   # Add both the parameters and return them."
#   total = arg1 + arg2
#   print ("Inside the function : ", total)
#   return total;

# Now you can call sum function
#total = sum( 10, 20 );
#print ("Outside the function : ", total)

#total
#################################################



