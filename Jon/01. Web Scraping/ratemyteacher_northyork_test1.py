#Grab the necessary information for AY Jackson

import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
req = Request('https://ca.ratemyteachers.com/ontario/north-york', headers={'User-Agent':'Mozilla/5.0'})
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
clean_school_name = BeautifulSoup(str_school_name, "lxml").get_text()

print(clean_school_name)

#next step get all the ratings
#then combine into df(?)
