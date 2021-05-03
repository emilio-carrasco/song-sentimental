import pandas as pd

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from textblob import TextBlob

def tokenize (string):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(string)
    return " ".join(tokens)

def stop_words (lista):
    stop_words = set(stopwords.words('english'))
    nueva_lista = []
    for string in lista:
        if string not in stop_words:
            nueva_lista.append(string)
    return " ".join(nueva_lista)
    
def intoEnglish(string):
    string = TextBlob(string)
    language= string.detect_language()
    if language !='en':
        try:
            english_blob = string.translate(language,to='en')
            return "".join(list(english_blob))
        except:
            return string
    else:
        return string
def stop_words (string):
    lista=string.split(' ')
    stop_words = set(stopwords.words('english'))
    nueva_lista = []
    for string in lista:
        if string not in stop_words:
            nueva_lista.append(string)
    return " ".join(nueva_lista)

def sentimentAnalysis(sentence):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(sentence)

def sentimental(cadena):
    tokens=tokenize(cadena)
    #english=intoEnglish(tokens)
    sw=stop_words(tokens)
    senti=sentimentAnalysis(sw)
    return senti 

