import requests
from bs4 import BeautifulSoup
import time

class Crawler:
    def __init__(self):
        self.stop = False
        self.urlList = []
        self.seed = 'https://en.wikipedia.org/wiki/Sustainable_energy'
        self.prefix = 'https://en.wikipedia.org'
        self.depth = 0
        self.depthSize = [0,0,0,0,0,0]
        self.focusedCrawler = False
        self.keyword = 'solar'
        self.task = 0
        self.doc = []   #To keep downloaded documents

    def getUserInput(self):
        self.task = input('Task 1: Crawling URL without keyword \nTask 2: BFS Webcrawler with keyword \nChoose the task (1 or 2): ')
        while self.task > 2 or self.task < 1:
            self.task = input('input either 1 or 2')
        self.seed = raw_input('Enter seed : ')
        if not self.seed:
            self.seed = 'https://en.wikipedia.org/wiki/Sustainable_energy'
        if self.task == 2:
            self.keyword = raw_input('Enter keyword : ')
        if not self.keyword:
            self.keyword = 'solar'

    def getLinksFromURL(self, url):
        linksList =[]
        try:
            htmlPage = requests.get(url)
        except:
            print "Problem in accessing ", url
            return linksList
        plainText = htmlPage.text
        soup = BeautifulSoup(plainText, "html.parser")

        mainBody = soup.find("div", {"id" : "mw-content-text"})
        for eachdivTag in mainBody.find_all('div', {'class' : 'reflist'}):
            eachdivTag.decompose()
        for eachdivTag in mainBody.find_all('div', {'class' : 'thumb'}):
            eachdivTag.decompose()
        for eachdivTag in mainBody.find_all('div', {'class' : 'navbox'}):
            eachdivTag.decompose()
        for eachdivTag in mainBody.find_all('table', {'class' : 'vertical-navbox'}):
            eachdivTag.decompose()

        htmlTags = mainBody.find_all("a")
        for tag in htmlTags:
            link = unicode(tag.get("href"))
            #print dir(link)
            notDuplicate = self.prefix + link not in linksList
            notDuplicate1 = self.prefix + link not in self.urlList
            if "wiki" in link and ":" not in link and "#" not in link\
                    and "Main_Page" not in link and ".org" not in link and "www." not in link\
                    and ".php" not in link and notDuplicate and notDuplicate1:
                    if self.task == 2:      #BFS crawler with keyword
                        if self.keyword.lower() in link.lower():
                            linksList.append(self.prefix + link)
                    else:
                        linksList.append(self.prefix + link)
        return linksList

    def saveIntoFile(self, fileName = "out.txt"):
        file = open(fileName, "w")
        for eachlink in self.urlList:
            file.write(eachlink + "\n")
        file.close()

    def bfsCrawler(self):
        Q = []
        self.urlList.append(self.seed)
        Q.append(self.seed)
        self.depthSize[self.depth] = 1
        while not self.stop:
            time.sleep(1)
            currentUrl = Q.pop(0)
            urlsPerPage = self.getLinksFromURL(currentUrl) #links in each page
            self.depthSize[self.depth] -= 1
            self.depthSize[self.depth + 1] += len(urlsPerPage)      #save number of URL's present in next depth level
            print currentUrl, self.depth + 1, len(self.urlList)
            if self.depthSize[self.depth] == 0:
                self.depth += 1
            for eachlink in urlsPerPage:
                if len(self.urlList) < 1000 and self.depth < 4:
                    Q.append(eachlink)
                    self.urlList.append(eachlink)
                else:                                     #to exit while loop if we captured 1000 urls
                    self.stop = True                      #and if depth reaches 5 (0-4)
                    break

        self.saveIntoFile()     #save final URL's into file



C = Crawler()
C.getUserInput()
C.bfsCrawler()

