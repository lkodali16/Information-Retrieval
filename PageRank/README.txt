This program is written in python 2.7
1) task2.py 	----> this file contains source code for PageRank Algorithm
2) task1_G1.txt ----> contains graph G1
3) task1.txt	----> report on simple statistics

Compiling:
	This program asks for a text file containing a graph in the format 
	mentioned in homework
	
	In linux shell, 
	$ python task2.py
	Enter the filename which contains graph: task1_G1.txt

	This print the output with page name(DocID) and page rank 
	
	For perplexity and top 50 pages:
	Uncomment the line 140 in the source code and re-run it.
	This will create two text files named, perplexity.txt and 
	pageranks.txt. 
	perplexity.txt contains perplexity values for each iteration
	pageranks.txt contains page name its rank for top 50 pages 