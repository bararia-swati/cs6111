import requests
import json
import time
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from preprocess import Preprocess


docdict = dict()

def run(JsonApiKey, EngineID, query,doc_id):
    url = "https://www.googleapis.com/customsearch/v1?key=" + JsonApiKey + "&cx=" + EngineID + "&q=" + query
    response = requests.get(url)
    GoogleResults = json.loads(response.text)['items']

    #STORE THE REQUIRED INFORMATION AS A LIST OF MAP 1
    res = []
    total = 0
    print("Google Search Results: ")
    print("======================")
    for entry in GoogleResults:
        if 'fileFormat' in entry.keys():
            continue
        else:
            total+=1
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
    return docdict,total

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
    SparseVectorUpdates = SparseVectorUpdates()

    while currentPrecision < precision:
        docdict,total = run(JsonApiKey, EngineID, query,doc_id)
        #print("docdict: ",docdict)
        if(total !=10):
            print("No of non-HTML results:",10-total)
        currentPrecision = float(calculate(docdict))
        if currentPrecision == 0.0:
            print("NO RELEVANT DOCUMENT FOUND TO EXPAND THE QUERY WITH")
            exit()
        print("Current Precision: ",currentPrecision)

        #new_doc_summaries= [doc_entry['snippet'] for doc_entry in docdict.values()]

        doc_dict_with_processed_snippets = get_processed_text_docdict(docdict)
        print("doc_dict_with_processed_snippets: ",doc_dict_with_processed_snippets)
        
        #Update Sparese Vector Dictionaries
        relevant_doc_dict= {doc_id: doc_entry for doc_id, doc_entry in doc_dict_with_processed_snippets.items() if doc_entry['relevance'] == True}
        non_relevant_doc_dict= {doc_id: doc_entry for doc_id, doc_entry in doc_dict_with_processed_snippets.items() if doc_entry['relevance'] == False}

        SparseVectorUpdates.update_all_relevant_doc_ids(relevant_doc_dict)
        SparseVectorUpdates.update_all_non_relevant_doc_ids(non_relevant_doc_dict)

        SparseVectorUpdates.update_relevant_term_frequency_dict(relevant_doc_dict)
        SparseVectorUpdates.update_non_relevant_term_frequency_dict(non_relevant_doc_dict)

        SparseVectorUpdates.update_document_frequency_dict(doc_dict_with_processed_snippets)



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