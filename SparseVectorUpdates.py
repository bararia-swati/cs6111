from collections import defaultdict, Counter
import math

class SparseVectorUpdates:
    def __init__(self, dictionary):
        self.all_relevant_doc_ids = set()
        self.all_non_relevant_doc_ids = set()
        self.relevant_term_frequency_dict = defaultdict(int)
        self.non_relevant_term_frequency_dict = defaultdict(int)
        self.document_frequency_dict = defaultdict(int)
        self.relevant_word_tfidf_scores_dict = defaultdict(float)
        self.non_relevant_word_tfidf_scores_dict = defaultdict(float)
        
        self.global_pos_tag_dict = defaultdict(list)

        self.query_vector = defaultdict(float)

    def initialize_query_vector(self, query):
        query_li = query.split()
        for term in query_li:
            self.query_vector[term] = -math.inf #to ensure it won't be chosen again
    
    def update_global_pos_tag_dict(self, doc_dict):
        for doc_id, doc_entry in doc_dict.items():
            pos_tag_dict = doc_entry['pos_tag_dict']
            
            for word, pos_tag in pos_tag_dict.items():
                self.global_pos_tag_dict[word] = pos_tag

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
    def update_tfidf_score_dictionaries(self,number_of_documents):
        score = 0.0
        tf=0.0
        idf=0.0

        for word, doc_id in self.relevant_term_frequency_dict.keys():
                tf = 1+ math.log(self.relevant_term_frequency_dict[(word,doc_id)])
                idf = math.log(number_of_documents/self.document_frequency_dict[word])
                tf_idf_score = tf*idf

                if self.global_pos_tag_dict[word] == 'NOUN':
                    tf_idf_score *= 1.5
                elif self.global_pos_tag_dict[word] == 'PROPN':
                    tf_idf_score *= 1.5
                elif self.global_pos_tag_dict[word] == 'ADJ':
                    tf_idf_score *= 1.0
                elif self.global_pos_tag_dict[word] == 'VERB':
                    tf_idf_score *= 0.5
                elif self.global_pos_tag_dict[word] == 'DET':
                    tf_idf_score *= 0.5
                
                
                self.relevant_word_tfidf_scores_dict[word] += tf_idf_score
        
        for word, doc_id in self.non_relevant_term_frequency_dict.keys():
                tf = 1+ math.log(self.non_relevant_term_frequency_dict[(word,doc_id)])
                idf = math.log(number_of_documents/self.document_frequency_dict[word])

                tf_idf_score = tf*idf

                if self.global_pos_tag_dict[word] == 'NOUN'
                    tf_idf_score *= 1.5
                elif self.global_pos_tag_dict[word] == 'PROPN':
                    tf_idf_score *= 1.5
                elif self.global_pos_tag_dict[word] == 'ADJ':
                    tf_idf_score *= 1.0
                elif self.global_pos_tag_dict[word] == 'VERB':
                    tf_idf_score *= 0.5
                elif self.global_pos_tag_dict[word] == 'DET':
                    tf_idf_score *= 0.5

                self.non_relevant_word_tfidf_scores_dict[word] += tf_idf_score       

    def update_query_vector_rocchios_algorithm(self, num_relevant_docs, num_non_relevant_docs, alpha=0.5, beta =0.5, gamma = 0.5):
        
        all_terms = set(self.relevant_word_tfidf_scores_dict.keys()).union(set(self.non_relevant_word_tfidf_scores_dict.keys()))
        
        for term in all_terms:
            delta = beta*(self.relevant_word_tfidf_scores_dict[term]/num_relevant_docs) - gamma*(self.non_relevant_word_tfidf_scores_dict[term]/num_non_relevant_docs)

            self.query_vector[term] = alpha* self.query_vector[term] + delta

        return 

    def select_query_expansion_terms(self, num_expansion_terms):
        sorted_query_vector = sorted(self.query_vector.items(), key=lambda x: x[1], reverse=True)
        selected_query_expansion_terms = [term for term, score in sorted_query_vector[:num_expansion_terms]]

        #set the scores of the selected terms to -inf so that they won't be selected again
        for term in selected_query_expansion_terms:
            self.query_vector[term] = -math.inf

        return selected_query_expansion_terms

        