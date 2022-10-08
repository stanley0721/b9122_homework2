from bs4 import BeautifulSoup
import urllib.request
import requests
import time
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"
seed_url_revised = "https://www.sec.gov/news/press-release/"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
texts=[]
dict={}

maxNumUrl = 1; #set the maximum number of urls to visit
print("Starting with url="+str(urls))

while len(urls) > 0 and len(opened) < maxNumUrl:
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
        time.sleep(0.2)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    soup = BeautifulSoup(webpage, "html.parser")  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url_revised, childUrl)
        text = tag.text
        if tag.text.lower().find('charges') !=-1 :
            dict[childUrl]=text
        if seed_url_revised in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)
print(dict)
first20 = list(dict.items())[:20]
print(first20)