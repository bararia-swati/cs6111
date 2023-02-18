#TFIDF Dictionary Updates

from collections import defaultdict, Counter
import math

class SparseVectorUpdates:
    def __init__(self, dictionary):
        self.all_relevant_doc_ids = set()
        self.all_non_relevant_doc_ids = set()
        self.relevant_term_frequency_dict = defaultdict(int)
        self.non_relevant_term_frequency_dict = defaultdict(int)
        self.document_frequency_dict = defaultdict(int)
        self.relevent_word_tfidf_scores_dict = defaultdict(float)
        self.non_relevent_word_tfidf_scores_dict = defaultdict(float)

    def update_all_relevant_doc_ids(self, docdict):
        for doc_id, doc_entry in docdict.items():
            self.all_relevant_doc_ids.add(doc_id)
    
    def update_all_non_relevant_doc_ids(self, docdict):
        for doc_id, doc_entry in docdict.items():
            self.all_non_relevant_doc_ids.add(doc_id)
    
    def update_relevant_term_frequency_dict(self, docdict):
        for doc_id, doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            for word in processed_snippet:
                self.relevant_term_frequency_dict[(word, doc_id)] += 1
    
    def update_non_relevant_term_frequency_dict(self, docdict):
        for doc_id, doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            for word in processed_snippet:
                self.non_relevant_term_frequency_dict[(word, doc_id)] += 1
    
    def update_document_frequency_dict(self, docdict):
        for doc_id, doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            word_freq_in_snippet = Counter(processed_snippet)
            for word in word_freq_in_snippet.keys():
                self.document_frequency_dict[word] += 1
#math.log(x/ y), 10)
    def score(self,docdict,total,flag):
        score = 0.0
        tf=0.0
        idf=0.0
        for doc_id, doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            for word in processed_snippet:
                if(flag==1):
                    tf = 1+ math.log(self.relevant_term_frequency_dict[(word,doc_id)])
                    idf = math.log(total/self.document_frequency_dict[word])
                    self.relevent_word_tfidf_scores_dict[word] += tf*idf
                else:
                    tf = 1+ math.log(self.non_relevant_term_frequency_dict[(word,doc_id)])
                    idf = math.log(10-total/self.document_frequency_dict[word])
                    self.non_relevent_word_tfidf_scores_dict[word] += tf*idf        


            
