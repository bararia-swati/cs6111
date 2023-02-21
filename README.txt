A.
Swati Bararia
sb4700
Jaidev Shah
js5161


B. 

List of files in the tar.gz
Search.py
SparseVectorUpdates.py
preprocess.py
laddered_query_ordering.py
project1_env.yml
README.txt

C. 
Commands necessary to install the required software and dependencies and then to run the program:
conda env create -f project1_env.yml
conda activate project1_env
python -m spacy download en_core_web_sm
python Search.py AIzaSyDI07bUpnPo2QrQaNRza54wYpz3BlldbRY e6d037c2c6089967e 0.8 "per se"


D.
Description:

We start by taking some necessary user inputs i.e Api Key, Engine Key, query, and precision. 

First, we preprocess and tokenize the query and obtain the relevant search string. Using this and the  above parameters we fetch the top 10 google search results. 

Feedback is taken from the user for each of the 10 results returned. Hence providing us with a binary label for relevance.

The title, url, snippet, relevance feedback of each result is stored in a dictionary. Non-HTML files are not considered out and not stored in the dictionary. 

Precision is calculated by observing how many out of the valid webpages were relevant.

If precision is below the desired precision, then the query is expanded

The snippet along with title is preprocessed to obtain a cleaner string which will be later used. 

The pre-processing includes removing stopwords, lemmatization, removing special characters, and a few other steps. (see the Preprocess class)
We compute a query vector which has relevance scores which are then sorted to find the top candidates for query expansion keywords. 

We also do query ordering using the corpus of relevant documents to obtain the most relevant order in which they should be used. 

Query is rerun for search results; feedback is taken and query expansion done until desired precision is reached.


E.
Query Expansion:

We use preprocessing to clean the title and snippet, strip it, stem it, remove stopwords, remove any special characters and other non-relevant items. We also do pos tagging of the words and finally append the processed snippet and pos tags dictionary to docdict. The nltk package is heavily used for these steps. 

Using the docdict, we create dictionaries (sparse vector representations) for tf, df for relevant and non-relevant. which further enable us to store term frequency for a term and corresponding doc_id. We also computer and store the document frequency mappings into a dictionary.

For every word, using the above information, we obtain the tf and idf score. We take the product of these, and then use the POS tags which we had initially given, to further augment the score based on what Part of Speech the word corresponds to. We scale the scores for noun/pronoun and reduce the scores for verb/preposition.

We use Rocchio's algorithm, with heuristically set values of alpha, beta, and gamma to obtain weights for each word which we haven�t already used in the query. We sort these in descending order of weights, and then take the top 2 terms from this, marking their weights in the query vector dictionary as negative infinity so that they are not chosen in future iterations. 

The user is again prompted to label relevance and we continue these iterations till the desired precision is reached.

Query Ordering: 
Once we have these new terms, and then combine these by using the index map of query into one huge corpus.
We create a single digit string of the form "ACBDAABCD..." and use this digit corpus  find the most frequent permutation of different sizes for the query terms. 
We pick the permutation with highest frequency, based on which we pursue the next iterations of the query.


F.
Google Custom Search Engine JSON API 

Key: AIzaSyDI07bUpnPo2QrQaNRza54wYpz3BlldbRY
Engine ID: e6d037c2c6089967e



