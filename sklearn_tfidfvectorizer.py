
def tfidf(documents, query):
    print("documents: ",documents)
    #create a vectorizer object
    vectorizer = TfidfVectorizer()

    #convert the documents into a document-term matrix
    doc_term_matrix = vectorizer.fit_transform(documents)
    print("Shape of doc_term_matrix: ",doc_term_matrix.shape)

    tfidf_scores = doc_term_matrix.toarray()

    query = [query]
    query_term_vector = vectorizer.transform(query)

    print("Shape of tfidf_scores: ",tfidf_scores.shape)
    print("Shape of query_term_vector: ",query_term_vector.shape)

    cosine_similarity = np.dot(query_term_vector.toarray(), tfidf_scores.T)
    query_norm = np.linalg.norm(query_term_vector.toarray())
    doc_norm = np.linalg.norm(tfidf_scores, axis=1)

    cosine_similarity = cosine_similarity / (query_norm * doc_norm)

    return tfidf_scores