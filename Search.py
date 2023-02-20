import requests
import json
import time
import os
import sys
import numpy as np
from preprocess import Preprocess
from SparseVectorUpdates import SparseVectorUpdates


docdict = dict()

def run(JsonApiKey, EngineID, query,doc_id):
    url = "https://www.googleapis.com/customsearch/v1?key=" + JsonApiKey + "&cx=" + EngineID + "&q=" + query
    response = requests.get(url)
    GoogleResults = json.loads(response.text)['items']

    #STORE THE REQUIRED INFORMATION AS A LIST OF MAP 1
    res = []
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
    print("JsonApiKey: ",JsonApiKey)
    print("EngineID: ",EngineID)

    print("ENTER THE SEARCH QUERY: ")
    query = input()
    print("ENTER THE Target Precision: ")
    precision = float(input())
    print()
    time.sleep(1)
    currentPrecision = 0.0
    doc_id =1
    SparseVectorUpdater = SparseVectorUpdates()

    query_preprocesser = Preprocess()
    preprocessed_query = query_preprocesser.preprocess(query)
    print("Preprocessed Query: ",preprocessed_query)
    SparseVectorUpdater.initialize_query_vector(preprocessed_query)


    while currentPrecision < precision:
        print("Current DocID index starts from: ",doc_id)
        docdict, NUM_VALID_WEBPAGES = run(JsonApiKey, EngineID, query,doc_id)

        doc_id += NUM_VALID_WEBPAGES

        #print("docdict: ",docdict)
        currentPrecision = float(calculate(docdict))
        if currentPrecision == 0.0:
            print("NO RELEVANT DOCUMENT FOUND TO EXPAND THE QUERY WITH")
            exit()
        print("Current Precision: ",currentPrecision)

        #new_doc_summaries= [doc_entry['snippet'] for doc_entry in docdict.values()]

        print("There are ",NUM_VALID_WEBPAGES," valid webpages" + "\n")

        doc_dict_with_processed_snippets = get_processed_text_docdict(docdict)
        print("doc_dict_with_processed_snippets: ",doc_dict_with_processed_snippets)
        
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