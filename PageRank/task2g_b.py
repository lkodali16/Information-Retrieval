#!/usr/bin/python2
import pdb
import math
import sys
import operator

in_links = open('wt2g_inlinks.txt','r')
read_in_links = in_links.readlines()

#sys.stdout = open('taskG2_output.txt','w')
#Remove newline character from each element
#for index in range(len(read_in_links)):
#  read_in_links[index] = read_in_links[index].strip("\n")

#Collect total pages
total_pages = []
total_pages_set = set()
inlinks_pages = {}
total_inlinks = set()
outlinks_pages = {}
results = {}
top_results = []

for index in range(len(read_in_links)):
  each = read_in_links[index].strip("\n")
  multiple_pages = each.split()
  total_pages.append(multiple_pages[0])
  total_pages_set.add(multiple_pages[0])
  inlinks_pages[multiple_pages[0]] = set()
  outlinks_pages[multiple_pages[0]] = set()

  # Add the inlinks of the destination link to a set
  for index in range(1,len(multiple_pages)):
  #Break the loop if the page doesn't have any inlinks
    try:
      inlinks_pages[multiple_pages[0]].add(multiple_pages[index])
      total_inlinks.add(multiple_pages[index])
    except:
      break
  
# Add the outlinks of each webpage 
for key in inlinks_pages.viewkeys():
  for element in inlinks_pages[key]:
      #try:      
    outlinks_pages[element].add(key)
      #except:
      # outlinks_pages[element]=set()
      # outlinks_pages[element].add(key)

#Collect the sink nodes i.e The pages that have no out links
sink_pages = total_pages_set.difference(total_inlinks)


#Page rank implementation for above graph
size=len(total_pages)
page_rank={}
page_perplexity={}
page_perplexity_diff={}
d = 0.85
entropy = 0

#Initital value
for page in total_pages:
  page_rank[page]= 1/float(size)
  page_perplexity[page]=[]
  page_perplexity_diff[page]=[]
 

#Calculate the page rank for each page in the considered graph.
for page in total_pages:
  while (len(page_perplexity_diff[page]) <= 4):
    entropy = 0
    for webpage in total_pages:
      entropy += page_rank[webpage]*(math.log(page_rank[webpage],2))
    entropy = -1*entropy
    perplexity=math.pow(2,entropy)
    page_perplexity[page].append(perplexity)
    if len((page_perplexity[page])) == 1:
      difference = abs(perplexity - page_perplexity[page][len(page_perplexity[page])-1])
    else:
      difference = abs(perplexity - page_perplexity[page][len(page_perplexity[page])-2])
    if difference < 1:
      page_perplexity_diff[page].append(1)
    else:
      page_perplexity_diff[page]=[]    
    sinkPR = 0
    for sinkpage in sink_pages:
      sinkPR += page_rank[sinkpage]
    newpage_rank={}

    for onpage in total_pages:
      newpage_rank[onpage] = (1-d)/size
      newpage_rank[onpage] += d*(sinkPR/size)
      for inlink in inlinks_pages[onpage]:
        newpage_rank[onpage] += d*(page_rank[inlink]/len(outlinks_pages[inlink]))

    for eachpage in total_pages:
      page_rank[eachpage] = newpage_rank[eachpage]

  print page,":",page_rank[page]
  #results[page]=page_rank[page]

sys.stdout.close()
'''
temporary_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
for x in range(0,50):
  top_results.append(temporary_results[x])  	
for element in top_results:
    print element[0],element[1]    
#sys.stdout.close()
'''
