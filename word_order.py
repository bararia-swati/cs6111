class Word_Order:

    def query_map(self, query):
        query_dic = dict()
        i=1
        query = query.split()
        for word in query:
            query_dic[word] = i
            i+=1
        return query_dic
    
    def map_query(self, query,query_map,new_bin_query):
        new_query = ""
        reverse_query_map = dict()
        query = query.split()
        for word in query:
            reverse_query_map[str(query_map[word])] = word
        for i in new_bin_query:
            new_query += " " + reverse_query_map[i]
        return new_query

    def combine(self, docdict,query_dict):
        corpus = ""
        for doc_id,doc_entry in docdict.items():
            if(doc_entry['relevance']==True):
                processed_snippet = doc_entry['processed_snippet']
                processed_snippet = processed_snippet.split()
                print(processed_snippet)
                for word in processed_snippet:
                    if(word in query_dict.keys()):
                        print(word)
                        corpus+= str(query_dict[word])
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
        for n in range(2,k+1):
            for i in range(len(clean_bin_corpus)-n+1):
                check_unique = set()
                for j in range(n):
                    check_unique.add(clean_bin_corpus[i+j])
                if(len(check_unique)==n):
                    if(clean_bin_corpus[i:i+n] in permutation_to_frequency.keys()):
                        permutation_to_frequency[clean_bin_corpus[i:i+n]]+=1
                    else:
                        permutation_to_frequency[clean_bin_corpus[i:i+n]]=1
                    if(max_frequency<permutation_to_frequency[clean_bin_corpus[i:i+n]]):
                        max_frequency = max(max_frequency,permutation_to_frequency[clean_bin_corpus[i:i+n]])
                        new_bin_query = clean_bin_corpus[i:i+n]
        return permutation_to_frequency,max_frequency,new_bin_query

    def order(self, query,docdict):
        query_map = self.query_map(query)
        print("1: ",query_map)
        bin_corpus = self.combine(docdict,query_map)
        print("2: ",bin_corpus)
        clean_bin_corpus = self.remove_consecutive(bin_corpus)
        print("3: ",clean_bin_corpus)
        k = len(query_map)
        permutation_to_frequency,max_frequency,new_bin_query = self.cal_frequency(k,clean_bin_corpus)
        print("4: ",permutation_to_frequency,new_bin_query)
        new_query = self.map_query(query,query_map,new_bin_query)
        return new_query

        
        
        


        
        
        

        





    




    
