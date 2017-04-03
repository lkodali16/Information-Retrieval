import requests
from bs4 import BeautifulSoup
import time

class Crawler:
    def __init__(self):
        self.seed = "https://en.wikipedia.org/wiki/Sustainable_energy"
        self.urlList = []
        self.keyword = 'solar'

    def dfsCrawler(self):
        self.urlList.append(self.seed)
        depth = 1
        self.crawler(self.seed, 1)

    def getUserInput(self):
        self.seed = raw_input('Enter seed : ')
        if not self.seed:
            self.seed = 'https://en.wikipedia.org/wiki/Sustainable_energy'
            self.keyword = raw_input('Enter keyword :')
        if not self.keyword:
            self.keyword = 'solar'

    def crawler(self, url, depth):
        linkList = []
        time.sleep(1)
        try:
            htmlPage = requests.get(url)
        except:
            print "Problem in accessing ", url
            return
        #print url, len(self.urlList), depth
        plainText = htmlPage.text
        soup = BeautifulSoup(plainText, "html.parser")

        mainBody = soup.find("div", {"id" : "mw-content-text"})
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
            #print "new link :" , link
            if "wiki" in link and ":" not in link and "#" not in link \
                    and "Main_Page" not in link and ".org" not in link and "www." not in link \
                    and ".php" not in link and self.keyword.lower() in link.lower():
                linkList.append(link)
        #print linkList
        for eachLink in linkList:
            notDuplicate = "https://en.wikipedia.org" + eachLink not in self.urlList
            if notDuplicate and len(self.urlList) < 1000:
                self.urlList.append("https://en.wikipedia.org" + eachLink)
                print 'https://en.wikipedia.org' + eachLink, len(self.urlList), "depth :", depth
                if depth < 5 and len(self.urlList) < 1000:
                    self.crawler("https://en.wikipedia.org" + eachLink, depth + 1)
                else:
                    return

    def saveIntoFile(self, fileName="outDFS.txt"):
        file = open(fileName, "w")
        for eachlink in self.urlList:
            file.write(eachlink + "\n")
        file.close()

w = Crawler()
w.getUserInput()
w.dfsCrawler()
w.saveIntoFile()
