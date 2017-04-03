import requests
from bs4 import BeautifulSoup
import time


def getLinksFromURL(url):
    linksList = []
    prefix = "https://en.wikipedia.org"
    try:
        htmlPage = requests.get(url)
    except:
        print "Problem in accessing ", url
        return linksList
    plainText = htmlPage.text
    soup = BeautifulSoup(plainText, "html.parser")

    mainBody = soup.find("div", {"id": "mw-content-text"})
    for eachdivTag in mainBody.find_all('div', {'class': 'reflist'}):
        eachdivTag.decompose()
    for eachdivTag in mainBody.find_all('div', {'class': 'thumb'}):
        eachdivTag.decompose()
    for eachdivTag in mainBody.find_all('div', {'class': 'navbox'}):
        eachdivTag.decompose()
    for eachdivTag in mainBody.find_all('table', {'class': 'vertical-navbox'}):
        eachdivTag.decompose()

    htmlTags = mainBody.find_all("a")
    for tag in htmlTags:
        link = unicode(tag.get("href"))
        #link = link.lower()
        # print dir(link)
        notDuplicate = link not in linksList
        # notDuplicate1 = prefix + link not in urlList
        if "wiki" in link and ":" not in link and "#" not in link \
                and "Main_Page" not in link and ".org" not in link and "www." not in link \
                and ".php" not in link and notDuplicate:
            # linksList.append(prefix + link)
            linksList.append(link[6:])

    return linksList

def buidGraph():
    graphDic = {}       # to store graph
    urlList = []        # stores 1000 links from file
    filename = raw_input('Enter filename: ')
    f = open(filename, 'r')     # open the file to read links
    for eachLine in f:      # construct dictionary
        # link = unicode(eachLink)
        #link = eachLine.lower()
        link = eachLine.replace("\n", "")
        urlList.append(link)
        graphDic[link[30:]] = []

    for eachLink in urlList:    # get every page corresponding to url in urlList and
                                # extract links from it. Then link those urls in graph
        print eachLink
        #time.sleep(1)
        links = getLinksFromURL(eachLink)
        for key in links:       # links in above links list will be key in graphDic and
                                # eachLink (source link) will be value
            if key in graphDic:
                graphDic[key].append(eachLink[30:])
    print graphDic

    f.close()
    f = open('graph.txt', 'w')
    for key in graphDic:
        f.write(key + ' ')
        for link in graphDic[key]:
            f.write(link + ' ')
        f.write('\n')
    f.close()

buidGraph()