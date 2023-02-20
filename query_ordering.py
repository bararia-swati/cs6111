class Query_Order:
    def __init__(self, query_li, original_initial_query_to_preprocessed_query_map):
        print("Inside Query_Order")
        self.query_li = query_li
        cleaned_query_li = []
        for term in query_li:
            if (term in original_initial_query_to_preprocessed_query_map):
                cleaned_query_li.append(original_initial_query_to_preprocessed_query_map[term])
            else:
                cleaned_query_li.append(term)

        self.cleaned_query_li = cleaned_query_li

        print("Inside Query_Order: cleaned_query_li: ", cleaned_query_li)

        self.cleaned_query = " ".join(cleaned_query_li)

        self.query_term_to_digit_map= self.construct_query_to_digit_map(self.cleaned_query_li)

    def construct_query_to_digit_map(self, query_li):
        query_to_digit_mapping = dict()
        i=1
        for word in query_li:
            query_to_digit_mapping[word] = i
            i+=1
        return query_to_digit_mapping
    
    def reconstruct_query(self,new_bin_query):
        ordered_query = list()
        reverse_digit_to_term_map = dict()

        #Obtain the Reverse Mapping ( from digit to word )
        for word in self.cleaned_query_li:
            digit = str(self.query_term_to_digit_map[word])
            reverse_digit_to_term_map[digit] = word

        ordered_query = list()
        for digit in new_bin_query:
            ordered_query.append( reverse_digit_to_term_map[digit] )

        return ordered_query

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

    def order_query(self,docdict):
        print("1: ",self.query_term_to_digit_map)
        bin_corpus = self.combine(docdict,self.query_term_to_digit_map)
        print("2: ",bin_corpus)
        clean_bin_corpus = self.remove_consecutive(bin_corpus)
        print("3: ",clean_bin_corpus)
        k = len(self.query_term_to_digit_map)
        permutation_to_frequency,max_frequency,new_bin_query = self.cal_frequency(k,clean_bin_corpus)
        print("4: ",permutation_to_frequency,new_bin_query)

        ordered_query_li = self.reconstruct_query(new_bin_query)
        print("5: ",ordered_query_li)

        return ordered_query_li

        
        
        


        
        
        

        





    




    
