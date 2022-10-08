from bs4 import BeautifulSoup
import urllib.request
import requests
#from urllib.request import Request

seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
seed_url_revised = "https://www.federalreserve.gov/newsevents/pressreleases/"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
list = []
list_of_covid = []

maxNumUrl = 5; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    soup = BeautifulSoup(webpage, "html.parser")  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url_revised, childUrl)
        if seed_url_revised in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)
            list.append(childUrl)

    for i in list:
        request = requests.get(url = i, headers={'User-Agent': 'Mozilla/5.0'})
        text = request.text
        set = BeautifulSoup(text, "lxml")
        texts = set.find('div', id = 'content')
        texts_content = texts.text.lower()
        if texts_content.find('covid') != -1:
            list_of_covid.append(i)
print(list_of_covid)