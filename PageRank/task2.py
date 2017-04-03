# Author: Lokesh Kodali
# Date: 02-25-2017
# iterative version of PageRank algorithm

from math import log, pow
import operator

class pageRank:
    def __init__(self):
        self.d = float(0.85)
        self.N = 0      # size of input
        self.P = {}
        self.PR = {}    # page rank for each page
        self.L = {}     # contains number of outlinks each page has
        self.S = []     # list containing sink nodes
        self.newPR = {}
        self.perplexity = []    # stores perplexity values for each iteration
        self.no_of_iterations = 4

    # read graph from the file and save into a dictionary
    def buildGraph(self):
        filename = raw_input("Enter the filename which contains graph: ")
        f = open(filename, 'r')

        for eachLine in f:
            eachLine.strip('\n')
            docIDs = eachLine.split()
            current_destination = docIDs.pop(0)     # first word is the destination page and rest are sources pointing to this page
            self.P[current_destination] = []
            for id in docIDs:
                self.P[current_destination].append(id)
        #print self.P
        self.N = len(self.P)
        f.close()

    # build sets S (sink nodes), M by removing duplicates, L (number of out-links from page)
    def extract_sets(self):
        for p in self.P:
            self.P[p] = list(set(self.P[p]))  # removing duplicates

        for p in self.P:
            self.L[p] = 0

        for p in self.P:
            for q in self.P[p]:
                self.L[q] += 1
        #print self.L

        for p in self.L:
            if self.L[p] == 0:
                self.S.append(p)
        #print self.S

    # check if the page rank is converged or not
    def converged(self):
        change_in_perplexity = 0
        entropy = 0
        for p in self.PR:
            entropy += self.PR[p] * log(self.PR[p], 2)
        current_perplexity = pow(2, -entropy)
        self.perplexity.append(current_perplexity)
        #print self.perplexity
        if len(self.perplexity) < self.no_of_iterations:
            return False
        else:
            for i in range(self.no_of_iterations):  #checks if consecutive change in perplexities is < 1
                if abs(self.perplexity[len(self.perplexity) - i -1] - self.perplexity[len(self.perplexity) - i-2]) < 1:
                    change_in_perplexity += 1
        if change_in_perplexity == self.no_of_iterations:
            return True
        else:
            return False
    # calculates the page rank using iterative version of pageRank Algorithm
    def calculate_pagerank(self):
        for p in self.P:
            self.PR[p] = float(1) / self.N

        while not self.converged():
            sinkPR = 0
            for p in self.S:
                sinkPR += self.PR[p]

            for p in self.PR:
                self.newPR[p] = (1 - self.d) / self.N
                self.newPR[p] += self.d * sinkPR / self.N
                for q in self.P[p]:
                    self.newPR[p] += self.d * self.PR[q] / self.L[q]

            for p in self.PR:
                self.PR[p] = self.newPR[p]

    def print_sets(self):
        print "page and page ranks are shown below:"
        sorted_pageranks = sorted(self.PR.items(), key=operator.itemgetter(1), reverse=True)
        pageranks = [x[1] for x in sorted_pageranks]
        pages = [x[0] for x in sorted_pageranks]
        for i in  range(len(pages)):
            print pages[i], '\t',  pageranks[i]


    def save_into_file(self):
        # save perplexity values into file
        print "Saving perplexity values into perplexity.txt ..."
        perplexity_file = open('perplexity.txt', 'w')
        for i in self.perplexity:
            perplexity_file.write(str(i) + '\n')
        perplexity_file.close()

        # sort the pageranks
        pagerank_file = open('pageranks.txt', 'w')
        sorted_pageranks = sorted(self.PR.items(), key=operator.itemgetter(1), reverse=True)

        pageranks = [x[1] for x in sorted_pageranks]
        pages = [x[0] for x in sorted_pageranks]
        for i in range(50):
            pagerank_file.write(str(pages[i]) + '\t' + str(pageranks[i]) + '\n')

        pagerank_file.close()

    def in_and_outlinks(self):
        inlinks = 0
        for key in self.P:
            if len(self.P[key]) == 0:
                inlinks += 1
        print "Number of pages with no\n1) inlinks: ", inlinks
        print "2) outlinks: ", len(self.S)
        pages_with_inlinksize = {}
        for page in self.P:
            pages_with_inlinksize[page] = len(self.P[page])
        sorted_inlinks = sorted(pages_with_inlinksize.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(5):
            print sorted_inlinks[i]


p = pageRank()      # creating an object for pageRank class
p.buildGraph()
p.extract_sets()
p.calculate_pagerank()
p.print_sets()
# p.save_into_file()      # only for graph with input size > 50 pages
# p.in_and_outlinks()     # for task 3

