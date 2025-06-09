import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "puzzles.settings")
import django
django.setup()

import re
import random
import numpy as np
import nltk
from nltk.corpus import abc
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
 
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

from wordsearch.models import Puzzle,Word,Char
import os


#from utils import generate_grids
model_path = os.path.join("artifacts","words.model")
os.makedirs(os .path.dirname(model_path),exist_ok=True)
print(model_path)

def build_model():
    text = abc.raw("science.txt") [:50000]
    text = sent_tokenize(text)
    corpus = []
    lemmatizer = WordNetLemmatizer()
    
    for sent in text:
        result = re.sub("[^a-zA-Z]"," ",sent)
        result = result.lower().split()
         
         
        result = [lemmatizer.lemmatize(word) for word in result if word not in set(stopwords.words("english")) and 3 < len(word) <= 7   ]
        result = " ".join(result)
        corpus.append(result)
        
    words = []
    print("preprocess compleated")
    for sent in corpus:
        sentence = sent_tokenize(sent)
        for word in sentence:
            words.append(simple_preprocess(word))
       
    print("tokenising compleated")
    model = Word2Vec(words,window=5,min_count=1,vector_size=20)
   
    model.save(model_path)
    print("modell saved!")
    return model

build_model()
 

 