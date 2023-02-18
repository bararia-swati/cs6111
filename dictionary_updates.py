#TFIDF Dictionary Updates

from collections import defaultdict

class SparseVectorUpdates:
    def __init__(self, dictionary):
        self.term_frequency_dict = defaultdict(int)
        self.document_frequency_dict = defaultdict(int)
        self.worf_tfidf_scores_dict = defaultdict(float)

    
    def update_term_frequency_dict(self, docdict):
        for doc_id, doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            for word in processed_snippet:
                self.term_frequency_dict[(word, doc_id)] += 1
    
    def update_document_frequency_dict(self, docdict):
        for doc_id, doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            for word in processed_snippet:
                self.document_frequency_dict[word] += 1


#git command to push to a branch
git push origin branch_name