__author__ = 'daksh'

from nltk.corpus import wordnet
import nltk
nltk.data.path.append("/home/daksh/Documents/Softwares/nltk_data")
from nltk.corpus import sentiwordnet as wn
from dishingOut.NPChunking.NPChunker import NPChunker
from textblob import Word

class AntonymReplacer(object):
    def __init__(self):
        self.chunker = NPChunker()
        self.chunker.train()

    def replace(self, adj, pos=None):
        '''antonyms = set()
        for syn in wordnet.synsets(adj, pos=pos):
            for lemma in syn.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.add(antonym.name())
        if len(antonyms) >= 1:
            return antonyms.pop()
        else:
            return None'''
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
        if len(antonyms) > 0:
            return antonyms[0]
        else:
            return None
    def replace_negations(self, sent):
        i, l = 0, len(sent)
        words = []
        flag = False
        while i < l:
            word = sent[i]
            if word == 'not' and i+1 < l:
                ant = self.replace(sent[i+1])
                if ant:
                    words.append(ant)
                    i += 2
                    flag = True
                    continue
            words.append(word)
            i += 1
        return flag,words

    def checkNegationWords(self,words):
        if 'not' in words:
            return True
        elif 'nothing' in words:
            return True
        else:
            return False

    def NegationCheck(self,sentence):

        words = self.chunker.getWords(sentence)
        flag,new_sent = self.replace_negations(words)
        if flag:
            return False,new_sent
        else:
            check = self.checkNegationWords(words)
            if check:
                return check,words
            else:
                return False,words



# a = AntonymReplacer()
# print(a.NegationCheck('The dosa was good'))