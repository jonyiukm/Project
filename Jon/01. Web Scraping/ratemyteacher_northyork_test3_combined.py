#Grab the necessary information for All schools in North York

############################
#   STEP 1 - SCHOOL NAME   #
############################

import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
req = Request('https://ca.ratemyteachers.com/ontario/north-york/1', headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()

#If lxml doesn't work, use html.parser instead
soup = BeautifulSoup(webpage,'lxml')

#Prettify() is meant to print the html nicely (can index like [:1000] for 1000 characters)
soup.prettify()

#DO NOT ASSIGN A NEW VARIABLE TO SOUP.PRETTIFY SINCE THAT WILL CHANGE THE TYPE TO STR
#NO FIND FOR STR TYPE
#USE TYPE(var_name) TO CHECK VARIABLE TYPE
#USE DIR(var_name) TO CHECK FUNCTIONS AVAILABLE FOR THAT VARIABLE TYPE

#school name is stored under h3 tag
name_tag_all = soup.findAll('h3',attrs={'class': 'school_name'})

#THis includes the chunk of h3 tags as well as the text value we are looking for
print(name_tag_all)

#remove all the tags within name_tag - .text.strip() doesn't work with bulk tags
#name_AY = name_tag.text.strip()
#convert the result to str, then use BeautifulSoup's get_text() to remove tags all at once
str_school_name = str(name_tag_all)
school_name = BeautifulSoup(str_school_name, "lxml").get_text()

#school_name above include all the \n and square bracket
#import re and use re.sub to remove these characters - | is OR and \ is escape 
import re

clean_school_name=re.sub('\'|\\n\n|\[|\]','',school_name)

print(clean_school_name)

type(clean_school_name)

#split the comma delimited string to list
clean_school_list = clean_school_name.split(",")

print(clean_school_list)

type(clean_school_list)
#################################
#   STEP 2 - INSTITUTION TYPE   #
#################################

#Institution type div class='institution_type'
institution_tag_all = soup.findAll('div',{'class': 'institution_type'})

print(institution_tag_all)

str_institution_type = str(institution_tag_all)

institution_type = BeautifulSoup(str_institution_type, "lxml").get_text()

institution_type

clean_institution_type=re.sub('\'|\\n\n|\[|\]','',institution_type)

print(clean_institution_type)

type(clean_institution_type)

#split the comma delimited string to list
clean_institution_list = clean_institution_type.split(",")

print(clean_institution_list)

type(clean_institution_list)

################################
#   STEP 3 - OVERALL RATINGS   #
################################

#Ratings type div class='rateit star-rating rateit-exclude'
#ratings_tag_all = soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'})

# this doesnt work --> test = soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'})['title']
#print(ratings_tag_all)

#str_ratings = str(ratings_tag_all)

#clean_ratings = BeautifulSoup(str_ratings, "lxml").get_text()

#print(clean_ratings)
# ABOVE RETURNS BLANK LIST --> NOT WORKING



ratings_tag_trial = soup.findAll('div',{'class': 'rateit star-rating rateit-exclude'})

clean_ratings_trial = []


for each_tag in ratings_tag_trial:
    clean_ratings_trial.append(each_tag["title"])

clean_ratings_trial

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

print(clean_ratings_count_final)

type(clean_ratings_count_final)

#split the comma delimited string to list
clean_ratings_count_list = clean_ratings_count_final.split(", ")

print(clean_ratings_count_list)

type(clean_ratings_count_list)

len(clean_ratings_count_list)
#str_ratings_1 = str(ratings_tag_all_1)

#clean_ratings_1 = BeautifulSoup(str_ratings_1, "html5lib")

#clean_ratings_1.findAll('div',{'class': 'rateit star-rating rateit-exclude'})['title']

#clean_ratings_1.findAll('div').get('title')



#html5lib
#next step get all the ratings
#then combine into df(?)

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
