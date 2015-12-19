__author__ = 'daksh'

import nltk
nltk.data.path.append("/home/daksh/Documents/Softwares/nltk_data")

from nltk.corpus import sentiwordnet as wn
from textblob import Word

def findantonyms(adj):
    antonyms=[]
    synonyms = []
    # word = Word(adj)
    # for syn in word.synsets[:]:
    for syn in list(wn.senti_synsets(adj)):
        # for l in syn.lemmas():
        for l in syn.synset.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(synonyms)
    print(antonyms)

findantonyms('bad')
