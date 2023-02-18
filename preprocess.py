
#Write a Class called Preprocess that has the following methods:
#remove_stopwords
#remove_punctuation_and_numbers
#lemmatize
#stem
#remove_short_words


import nltk
import spacy
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import string

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Preprocess:
    def __init__(self):
        self.stopwords = stopwords.words('english')
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.spacy_nlp= spacy.load('en_core_web_sm')
        self.punctuation = string.punctuation
        self.numbers = string.digits

    def remove_special_characters(self, text):
        text= re.sub('[^A-Za-z0-9]+', ' ', text)
        text = text.replace(u'\xa0', u' ')
        return text


    def lowercase(self, text):
        return text.lower()


    def remove_stopwords(self, text):
        return [word for word in text if word not in self.stopwords]

    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))

    def remove_duplicate_spaces(self, text):
        return re.sub(' +', ' ', text)

    def lemmatize(self, text):
        return [self.lemmatizer.lemmatize(word) for word in text]

    def stem(self, text):
        return [self.stemmer.stem(word) for word in text]

    def remove_short_words(self, text):
        return [word for word in text if len(word) > 2]
    
    def pos_tagging(self, text):
        #Spacy POS Tagging
        
        doc = self.spacy_nlp(text)
        token_to_pos = {}
        for token in doc:
            token_to_pos[token.text] = token.pos_

        return token_to_pos

    def preprocess(self, text):
        text = self.remove_special_characters(text)
        text = self.lowercase(text)
        pos_tags_dict = self.pos_tagging(text)
        print("pos_tags_dict: ",pos_tags_dict)

        text = self.remove_punctuation(text)

        text = self.remove_duplicate_spaces(text)
        text = text.split()
        
        text = self.remove_stopwords(text)
        text = self.lemmatize(text)

        processed_text= ' '.join(text)

        return processed_text, pos_tags_dict


TextProcessor = Preprocess()

original_text = "This is a test sentence. It has punctuation, numbers 123, and short words like a, an, and the."
print("Original Text: ", original_text)
processed_text = TextProcessor.preprocess(original_text)
print("Processed Text: ", processed_text)

#Write a Class called Search that has the following methods:
#run
#calculate
#



