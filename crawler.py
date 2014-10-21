'''
Created on Sep 21, 2014
@author: Swapna Bhi
'''

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import sys
import time

# Function to check if the given url is valid
# Argument: url - url to be checked for validity
# criteria for validity :
# 1.  Not in visited set
# 2.  Not Main_page or wiki page url
# 3.  In Wikipedia's domain
# 4.  Does not contain ':'
# Returns : Boolean
def validLink(url):
    if url not in visited and url!="http://en.wikipedia.org/wiki/" and url!="http://en.wikipedia.org/wiki/Main_Page" and url.startswith('http://en.wikipedia.org/wiki/') and url.count(':') == 1 :
        return True
    else:
        return False
    
# Function to crawl current page
# Argument: url - url for this page to scrap
#           key - keyphrase to look for
#           currdepth - current depth
# Returns: list of links on this page
def crawlpage(url,key,currdepth):
    currUrls = []
    append= currUrls.append
    join=urllib.parse.urljoin
    try:
            htmltext = urllib.request.urlopen(urls[0])
            # 1 second delay as courtesy 
            time.sleep(1) 
            the_text = htmltext.read()
            # converting the text in lowercase for keyphrase search
            textStr = str(the_text).lower()                
    except:
            print('no idea what is happening ',  sys.exc_info())
         
    soup = BeautifulSoup(the_text)
    soup.prettify('utf-8')
    # get canonical link from the document
    canon = soup.find("link", {"rel":"canonical"})
    canonicalurl = canon['href']
    # we will be dealing with canonical url and not with the url given in document
    if canonicalurl not in visited and key.lower() in textStr:
        visited.add(canonicalurl)
        file.write(canonicalurl + '\n')
        # Design decision :
        # We will not need any links from pages at depth 3
        # so I will be skipping them.
        # This increases the speed of the program byh atleast 10%
        # No a good idea for actual crawler
        if currdepth !=2:
            for tag in soup.findAll('a', href=True):
                x= tag['href']
                link = join(url,x)
                # trim string from #
                # actually not needed because of cannonical urls
                # used as added performace enhancement
                link = link.split('#')[0]
                if validLink(link):
                    append(link)
    soup.decompose()
    htmltext.close()
    return currUrls            
                
            
            
# Function to crawl all pages in this level
# Argument: urlsToCrawl - list of urls to crawl. All urls have parents on same level 
#           key - keyphrase to look for
#           level - current depth
# Returns: list of links on this page            
def crawlBFS(urlsToCrawl, key, level):
    thislevelurl = []
    # crawl all urls in this level one by one
    while len(urlsToCrawl) > 0:
        thisUrl= urlsToCrawl[0]
        if thisUrl not in visited:
            thislevelurl = thislevelurl + crawlpage(thisUrl,key,level)
        urlsToCrawl.pop(0)
    return thislevelurl

# The program takes input from user directly
# so we do not need to provide any arguments
seed = input('Type in a seed you want to use : ')
keyPhrase = input('Type the key phrase : ')

# visited : set of all urls visited so far
# urls : list of urls to visit in next level
visited = set()
urls = []

# added seed page to urls
urls.append(seed)
depth = 0

# all urls visited till level 3 are stored in a file
# name: newfile.txt
# location : same as spider.py file
file = open("newfile.txt", "w")
# repeat till level 3 or depth 2
while depth < 3:
    urls = crawlBFS(urls,keyPhrase,depth)
    print('Till level ', depth, 'I crawled ', len(visited))
    depth +=1
    
file.close()    
   

        
    