class word_order:

    def query_map(self, query):
        query_dic = dict()
        i=1
        for word in query:
            query_dic[word] = i
            i+=1
        return query_dic
    
    def map_query(self, query,query_map,new_bin_query):
        new_query = ""
        reverse_query_map = dict()
        for word in query:
            reverse_query_map[query_map[word]] = word
        for i in new_bin_query:
            new_query += " " + reverse_query_map[i]
        return new_query

    def combine(self, docdict,query_dict):
        corpus = ""
        for doc_entry in docdict.items():
            processed_snippet = doc_entry['processed_snippet']
            for word in processed_snippet:
                if(word in query_dict.keys()):
                    corpus+= query_dict[word]
        return corpus
        
    def remove_consecutive(self, bin_corpus):
        clean_bin_corpus = ""
        prev = "0"
        for i in bin_corpus:
            if(i!=prev):
                clean_bin_corpus+=i
            prev=i
        return clean_bin_corpus

    def cal_frequency(self,k,clean_bin_corpus):
        permutation_to_frequency = dict()
        max_frequency = 0
        new_bin_query = ""
        for n in range(k-2,k+1):
            for i in range(len(clean_bin_corpus)-n):
                check_unique = set()
                for j in range(n):
                    check_unique.add(clean_bin_corpus[i+j])
                if(len(check_unique)==n):
                    if(clean_bin_corpus[i:i+n] in permutation_to_frequency.keys()):
                        permutation_to_frequency[clean_bin_corpus[i:i+n]]+=1
                    else:
                        permutation_to_frequency[clean_bin_corpus[i:i+n]]=1
                    max_frequency = max(max_frequency,permutation_to_frequency[clean_bin_corpus[i:i+n]])
                    new_bin_query = clean_bin_corpus[i:i+n]
        return permutation_to_frequency,max_frequency,new_bin_query

    def order(self, query,docdict):
        query_map = query_map(query)
        bin_corpus = self.combine(docdict,query_map)
        clean_bin_corpus = self.remove_consecutive(bin_corpus)
        k = len(query_map)
        permutation_to_frequency,max_frequency,new_bin_query = self.cal_frequency(k,clean_bin_corpus)
        new_query = self.map_query(query,query_map,new_bin_query)
        return new_query

        
        
        


        
        
        

        





    




    
