import sys
import nltk
from enum import Enum
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords


type = None
stemmer = None
lemmatizer = None
stopWords = None
stemmer = PorterStemmer() #set stemmer
lemmatizer = WordNetLemmatizer() #set lemmatizer
stopWords = stopwords.words("english") #english stop words def


def parseTokensFromText(text):
    tokenList = nltk.word_tokenize(text)
 #   t=nltk.pos_tag(tokenList)
 #   if self.type == ParserType.wordprocessing:
    parsedTokenList = [applyTextProcessing(token.lower()) for token in tokenList if (token.isalpha()) and (not token.lower() in stopWords)]
  #  else:
  #      parsedTokenList = [token.lower() for token in tokenList if token.isalpha()]

    return parsedTokenList


def applyTextProcessing( token):
    stemmedToken = applyStemming(token)
    #return stemmedToken
    return applyLemmatization(stemmedToken)

def applyStemming(token):
    """applies the stemming algorithm to the given token"""
    return stemmer.stem(token)

def applyLemmatization(token):
    return lemmatizer.lemmatize(token)
