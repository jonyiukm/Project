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

#create a test function to convert province and city with hyphens and get the last page
#if only 1 page, the find('li') will be None
#write an if clause to say is not None, and convert city_name and province to no space
def scrape(province_1, city_name_1):
    if ' ' in city_name_1 == True:
        city_name=city_name_1.replace(' ','-')
        #create website from city_name
    else:
        city_name=city_name_1
        
    if ' ' in province_1 == True:
        province=province_1.replace(' ','-')
    else:
        province=province_1
        
    base_url = 'https://ca.ratemyteachers.com/' + str(province) + '/' + str(city_name) + '/'
    r0 = Request(base_url, headers={'User-Agent':'Mozilla/5.0'})        
    c0 = urlopen(r0).read()
    soup0 = BeautifulSoup(c0,'lxml')
    
    if soup0.find('li', attrs={'class':'last_page'}) is not None:
        last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1]    
    else:
        last_pg='1'
    
    return city_name

#create a function which takes city name as input
scrape("New Brunswick","Ste Anne De Madawaska")


rt = Request('https://ca.ratemyteachers.com/new-brunswick/ste-anne-de-madawaska', headers={'User-Agent':'Mozilla/5.0'})
ct = urlopen(rt).read()
soupt = BeautifulSoup(ct,'lxml')
last_pg_t=soupt.find('li', attrs={'class':'last_page'}).a['href'][-1]    

last_pg_t=soupt.find('li', attrs={'class':'last_page'})

last_pg_t


#Base URL and get the last page in string
base_url = 'https://ca.ratemyteachers.com/ontario/north-york/'
r0 = Request(base_url, headers={'User-Agent':'Mozilla/5.0'})        
c0 = urlopen(r0).read()
soup0 = BeautifulSoup(c0,'lxml')
last_pg=soup0.find('li', attrs={'class':'last_page'}).a['href'][-1]    


##########################################################################################
#   STEP 10 - Setup time interval for scraping the data to prevent crashing the server   #
##########################################################################################