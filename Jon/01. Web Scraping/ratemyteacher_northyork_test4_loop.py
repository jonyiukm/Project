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


#####################################################
#   STEP 0 - FIND NUMBER OF PAGES TO LOOP THROUGH   #
#####################################################


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

rating_tag_all

for container in rating_tag_all:
    if container["title"] != '':
        ratings.append(container["title"])

ratings.remove(ratings[0])

ratings

count_tag_all = soup.findAll('div',{'class': 'rating_count'})

count_tag_all

count_tag_all[0].text.strip())


for container in count_tag_all:
    count = container.text.strip()
    number_of_reviews.append(count)            
    
number_of_reviews

number_of_reviews = re.sub('\'|\\n|\[|\]','',number_of_reviews)

ratings_count = BeautifulSoup(str_ratings_count, "lxml").get_text()

ratings_count

clean_ratings_count=re.sub('\'|\\n|\[|\]','',ratings_count)

clean_ratings_count_1 = clean_ratings_count.replace('ratings','')

clean_ratings_count_final = clean_ratings_count_1.replace('rating','')

clean_ratings_count_list = clean_ratings_count_final.split(", ")

#to remove the city rating and the last two rateit tag which doesn't contribute to any values
clean_ratings_all = clean_ratings_trial[1:-2]
clean_ratings_all
len(clean_ratings_all)

#get page number

https://towardsdatascience.com/an-introduction-to-web-scraping-with-python-bc9563fe8860