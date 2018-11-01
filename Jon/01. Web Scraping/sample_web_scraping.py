import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
req = Request('https://amzn.to/2m7iUGH', headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()

#If lxml doesn't work, use html.parser instead
soup = BeautifulSoup(webpage,'lxml')

#Prettify() is meant to print the html nicely (can index like [:1000] for 1000 characters)
soup.prettify()

#DO NOT ASSIGN A NEW VARIABLE TO SOUP.PRETTIFY SINCE THAT WILL CHANGE THE TYPE TO STR
#NO FIND FOR STR TYPE
#USE TYPE(var_name) TO CHECK VARIABLE TYPE
#USE DIR(var_name) TO CHECK FUNCTIONS AVAILABLE FOR THAT VARIABLE TYPE

span = soup.find('span',{'id': 'priceblock_ourprice'})
print(span)