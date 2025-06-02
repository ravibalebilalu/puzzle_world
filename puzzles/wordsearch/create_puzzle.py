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

from utils import generate_grids

 

print("entry")

def build_model():
    text = abc.raw("science.txt") 
    text = sent_tokenize(text)
    corpus = []
    lemmatizer = WordNetLemmatizer()
    
    for sent in text:
        result = re.sub("[^a-zA-Z]"," ",sent)
        result = result.lower().split()
        result = [lemmatizer.lemmatize(word) for word in result if word not in set(stopwords.words("english"))]
        result = " ".join(result)
        corpus.append(result)
        print(result)
    words = []
    print("preprocess compleated")
    for sent in corpus:
        sentence = sent_tokenize(sent)
        for word in sentence:
            words.append(simple_preprocess(word))
            print(word)
    print("tokenising compleated")
    model = Word2Vec(words,window=5,min_count=2,vector_size=20)
    print("modelling compleated")
    return model

model_words = build_model()
words = model_words.wv.index_to_key
print(f'Words : {words}')
final = [word for word in words if 3 <= len(word) <= 7]

print("choice started")


 
 
 


for c in range(200):
    start = time.time()
    choice = random.sample(final, 10)
    print(f"choice : {choice}")
    puzzle = Puzzle(row_length=12, col_length=12)  # set your desired size
    puzzle.save()
    grid, placed_words = generate_grids(puzzle, choice)
    print("grid and words placed")

    print(f"{c} : saved in {time.time() - start:.2f} sec")

