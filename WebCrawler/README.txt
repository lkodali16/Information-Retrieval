Program for this homework is written in Python 2.7
1) bfs.py -----> this file contains both Task 1 and Task 2-A
2) dfs.py -----> this file contains Task 2-B


These programs require bs4 module, requests library to run

compiling :
	In Linux command line,
	
	For Task 1:
		$ python bfs.py
	Programs asks for selecting task 1 or 2. choose task 1 by giving "1" as input
	Next it asks seed as input. Input seed URL or press enter for default URL given in homework
	This will print URL which is currently being requested from network, depth at which URL is present, size of URL's list crawled (or saved)
	Output is saved in "out.txt" file

	For Task 2-A:
		$ python bfs.py
	Choose task 2 by entering number 2
	Enter seed URL and keyword or press enter for default input (as in homework)
	
	For Task 2-B:
		$ python dfs.py
	Enter seed and then enter keyword
	Program prints out URL which is currently being requested from internet, number of URL's extraced upto that point, current depth
	Output is saved in outDFS.txt
