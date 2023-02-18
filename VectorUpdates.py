#Write a function that computes tf-idf scores given a list of documents and a query
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import math
import pandas as pd

def tfidf(documents, query):

    #create a vectorizer object
    vectorizer = TfidfVectorizer()

    #convert the documents into a document-term matrix
    doc_term_matrix = vectorizer.fit_transform(documents)

    #compute tf-idf scores
    tfidf_scores = doc_term_matrix.toarray()

    #compute the query term vector
    query_term_vector = vectorizer.transform(query)

    #compute the cosine similarity between the query and each document
    cosine_similarity = np.dot(query_term_vector.toarray(), tfidf_scores.T)

    #compute the euclidean norm of the query term vector
    query_norm = np.linalg.norm(query_term_vector.toarray())

    #compute the euclidean norm of each document term vector
    doc_norm = np.linalg.norm(tfidf_scores, axis=1)

    #compute the cosine similarity between the query and each document
    cosine_similarity = cosine_similarity / (query_norm * doc_norm)

    #return the cosine similarity
    return cosine_similarity
