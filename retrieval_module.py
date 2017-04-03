import os
import glob
import math
import string
import operator
import indexer

class Retriever:
    def __init__(self, corpus_directory):
        self.corpus_directory = corpus_directory
        # parser = indexer.Parser()
        self.I = indexer.InvertedIndexer(self.corpus_directory)
        self.query_dic = {}  # stores the parsed query and its frequency
        self.score_dic = {}  # scores of each document
        self.current_query = ''     # used to open the file with query name and save results
        self.query_id = 0

    def build_indexes(self):
        # parser = indexer.Parser()
        # parser.build_corpus(self.raw_corpus_directory)
        # I = indexer.InvertedIndexer(self.raw_corpus_directory)
        self.I.ngram_indexer(1)

    def get_scores_for_docs(self):
        avdl = 0;       # average doc length
        # initialize score_dic to zero
        for each_doc in self.I.doc_legths:
            avdl += self.I.doc_legths[each_doc]
        avdl = float(avdl)/len(self.I.doc_legths)
        for each_file in self.I.docIDs:
            BM25_score = 0
            for each_query in self.query_dic:
                BM25_score += self.calculate_BM25_score(each_query, self.I.docIDs[each_file], avdl)
            self.score_dic[each_file] = BM25_score

        # sort the documents based on scores
        sorted_docs = sorted(self.score_dic.items(), key=operator.itemgetter(1), reverse=True)
        docs = [x[0] for x in sorted_docs]
        scores = [x[1] for x in sorted_docs]

        # print self.score_dic
        # save results in to a file
        if os.getcwd() == self.corpus_directory:
            os.chdir(os.pardir)
        f = open(self.current_query + '.txt', 'w')
        for i in range(100):
            f.write(str(self.query_id) \
                    + " Q0 " \
                    + str(docs[i]) + ' ' \
                    + str((i+1)) + " " \
                    + str(scores[i]) + " " \
                    + "system_name\n")
        f.flush()
        f.close()


    def calculate_BM25_score(self, query, docID, avdl):     # query - single word in the whole query
        BM25_score_per_query = 0
        N = len(self.I.docIDs)
        n = 0
        f = 0
        if query in self.I.inverted_indexes:
            n = len(self.I.inverted_indexes[query])
            if docID in self.I.inverted_indexes[query]:
                f = self.I.inverted_indexes[query][docID]
        qf = self.query_dic[query]
        k1 = 1.2
        b = 0.75
        k2 = 100
        dl = self.I.doc_legths[docID]
        K = k1*((1-b) + (b*(dl/avdl)))
        BM25_score_per_query = math.log(((float(N) - n + 0.5) / (n + 0.5))) * \
                               (float((k1 + 1)*f) /(K+f)) * \
                               ((float((k2 + 1) * qf)) / float(k2 + qf))

        return BM25_score_per_query


    def process_query(self, query):
        self.query_id += 1
        query = query.lower()
        self.current_query = query
        tokens = query.split()
        self.query_dic = {}
        for each_token in tokens:
            self.query_dic[each_token] = 0
        for each_token in tokens:
            self.query_dic[each_token] += 1     # term frequency


directory = raw_input('Enter corpus directory: ')
if not os.path.exists(directory):
    print "Please enter valid directory address"
    directory = raw_input()
r = Retriever(directory)
r.build_indexes()
e = False   # e - exit
while not e:
    query = raw_input("Enter the Query: ")
    while not query:
        query = raw_input("Enter the Query: ")
    if query == 'e':
        e = True
        break
    r.process_query(query)
    r.get_scores_for_docs()




