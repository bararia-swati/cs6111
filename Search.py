import requests
import json
import time
import os
import sys
import numpy as np
from preprocess import Preprocess
from SparseVectorUpdates import SparseVectorUpdates
from laddered_query_ordering import Laddered_Query_Order


def run(JsonApiKey, EngineID, query, doc_id):
    url = "https://www.googleapis.com/customsearch/v1?key=" + JsonApiKey + "&cx=" + EngineID + "&q=" + query
    response = requests.get(url)
    GoogleResults = json.loads(response.text)['items']

    #STORE THE REQUIRED INFORMATION AS A LIST OF MAP 1
    res = []
    docdict = dict()
    print("Google Search Results: ")
    print("======================")

    NUM_VALID_WEBPAGES = 0
    for entry in GoogleResults:
        if 'fileFormat' in entry.keys():
            continue
        title, link, website, snippet = "", "", "", "--(empty)--"
        if 'title' in entry.keys ():
            title = entry['title']
        if 'link' in entry.keys():
            link = entry['link']
        if 'snippet' in entry.keys():
            snippet = entry['snippet']
        entry = {"title": title, "link": link, "snippet": snippet, "relevance": False}
        res.append(entry)
        docdict[doc_id] = entry
        doc_id += 1

        NUM_VALID_WEBPAGES += 1

    for doc_id, doc_entry in docdict.items():
        print("RESULT " + str(doc_id))
        print("[")
        
        print("URL: " + doc_entry['link'])
        print("Title: " + doc_entry['title'])
        print("Summary: " + doc_entry['snippet'])
        print("]")
        print("Relevant (Y/N)? ")
        check = input()
        print()
        if check == 'Y' or check == 'y':
            doc_entry ['relevance'] = True
        else:
            doc_entry ['relevance'] = False
    return docdict, NUM_VALID_WEBPAGES

def calculate(docdict):
    #calculates precision@10
    #returns precision
    count = 0.0
    for doc_id, doc_entry in docdict.items():
        if doc_entry['relevance'] == True:
            count += 1
    return count/10

def main():
    #JsonApiKey, EngineID = "AIzaSyDI07bUpnPo2QrQaNRza54wYpz3BlldbRY", "e6d037c2c6089967e"
    JsonApiKey = sys.argv[1]
    EngineID = sys.argv[2]
    precision = float(sys.argv[3])
    query = sys.argv[4]
    time.sleep(1)
    currentPrecision = 0.0
    doc_id =1
    SparseVectorUpdater = SparseVectorUpdates()

    query_preprocesser = Preprocess()
    preprocessed_initial_query, query_pos_tag_dict = query_preprocesser.preprocess(query)
    #print("Preprocessed Initial Query: ",preprocessed_initial_query)
    SparseVectorUpdater.initialize_query_vector(preprocessed_initial_query)

    #Map from preprocessed query to initial query original
    preprocessed_query_to_original_query_map = dict()
    preprocessed_query_to_original_query_map[preprocessed_initial_query] = query
    original_initial_query_to_preprocessed_query_map = dict()
    original_initial_query_to_preprocessed_query_map[query] = preprocessed_initial_query

    query_li = query.split()

    while currentPrecision < precision:
        #print("Current DocID index starts from: ",doc_id)
        print("Parameters:")
        print("Client key  = ",JsonApiKey)
        print("Engine key  = ",EngineID)
        
        original_format_query_li = list()
        for query_term in query_li:
            if query_term in preprocessed_query_to_original_query_map:
                original_format_query_li.append(preprocessed_query_to_original_query_map[query_term])
            else:
                original_format_query_li.append(query_term)

        original_format_query = " ".join(original_format_query_li)
        #print(" New Query : ",original_format_query)
        print("Query       = ",original_format_query)
        print("Precision   = ",precision)
        docdict, NUM_VALID_WEBPAGES = run(JsonApiKey, EngineID, original_format_query,doc_id)

        doc_id += NUM_VALID_WEBPAGES
        #print("docdict: ",docdict)
        currentPrecision = float(calculate(docdict))
        print("======================")
        print("FEEDBACK SUMMARY")
        print("Query ",query)
        print("Precision ",currentPrecision)
        if(currentPrecision<precision):
            print("Still below the desired precision of ",precision)
        if currentPrecision == 0.0:
            print("Below desired precision, but can no longer augment the query")
            exit()
        print("Indexing results ....")
        print("Indexing results ....")
        #print("Current Precision: ",currentPrecision)

        #print("There are ",NUM_VALID_WEBPAGES," valid webpages" + "\n")

        doc_dict_with_processed_snippets = get_processed_text_docdict(docdict)
        
        #Update Global POS Tag Dictionary
        SparseVectorUpdater.update_global_pos_tag_dict(doc_dict_with_processed_snippets)

        #Update Sparse Vector Dictionaries
        relevant_doc_dict= {doc_id: doc_entry for doc_id, doc_entry in doc_dict_with_processed_snippets.items() if doc_entry['relevance'] == True}
        non_relevant_doc_dict= {doc_id: doc_entry for doc_id, doc_entry in doc_dict_with_processed_snippets.items() if doc_entry['relevance'] == False}

        relevant_doc_ids = list(relevant_doc_dict.keys())
        non_relevant_doc_ids = list(non_relevant_doc_dict.keys())
        num_relevant_docs = len(relevant_doc_ids)
        num_non_relevant_docs = len(non_relevant_doc_ids)

        #Just updating list of all relevant and non-relevant doc_ids seen so far
        SparseVectorUpdater.update_all_relevant_doc_ids(relevant_doc_dict)
        SparseVectorUpdater.update_all_non_relevant_doc_ids(non_relevant_doc_dict)

        #Updating the term frequency dictionaries
        SparseVectorUpdater.update_relevant_term_frequency_dict(relevant_doc_dict)
        SparseVectorUpdater.update_non_relevant_term_frequency_dict(non_relevant_doc_dict)

        #Updating the document frequency dictionaries
        SparseVectorUpdater.update_document_frequency_dict(doc_dict_with_processed_snippets)

        #TF IDF Scores Computation
        SparseVectorUpdater.update_tfidf_score_dictionaries(NUM_VALID_WEBPAGES)

        #Updating Query Vector with Modified Rocchios Algorithm 
        ALPHA = 0.5
        BETA = 0.5
        GAMMA = 0.5
        SparseVectorUpdater.update_query_vector_rocchios_algorithm(num_relevant_docs, num_non_relevant_docs, ALPHA, BETA, GAMMA)

        # Select Query Expansion Terms
        NUM_QUERY_EXPANSION_TERMS = 2
        query_expansion_terms = SparseVectorUpdater.select_query_expansion_terms(NUM_QUERY_EXPANSION_TERMS)

        print("Augmenting by ",query_expansion_terms)

        query_li.extend(query_expansion_terms)

        query = query + " " + " ".join(query_expansion_terms)

        #Now, query ordering
        Query_Orderer = Laddered_Query_Order(query_li, original_initial_query_to_preprocessed_query_map)
        ordered_query_li = Query_Orderer.execute(docdict)
        #print("Ordered Query Li: ",ordered_query_li)

        #if length of ordered_query_li < query_li (i.e. if best permutation through our algorith has a lower length match), simply default to adding the previous terms to the beginning of the ordered_query_li
        if len(ordered_query_li) < len(query_li):
            for query_term in query_li:
                if query_term not in ordered_query_li:
                    ordered_query_li.insert(0,query_term)

        query_li = ordered_query_li


    #pring global pos tag dict
    # print("Global POS Tag Dictionary: ",SparseVectorUpdater.global_pos_tag_dict)
    # print('Target Precision Reached')

def get_processed_text_docdict(docdict):
    #preprocess the text
    #returns the processed text
    preprocessor = Preprocess()
    for doc_id, doc_entry in docdict.items():
        doc_text = doc_entry['snippet']
    
        processed_text, pos_tag_dict = preprocessor.preprocess(doc_text)
        docdict[doc_id]['processed_snippet'] = processed_text
        docdict[doc_id]['pos_tag_dict'] = pos_tag_dict
    
    return docdict


if __name__ == '__main__':
    main()