__author__ = "Daksh"

import nltk
import csv
import json
from dishingOut.NPChunking.NPChunker import NPChunker


nltk.data.path.append("/home/daksh/Documents/Softwares/nltk_data")

from nltk.corpus import sentiwordnet as wn
from textblob import Word


pos_words = list()
neg_words = list()
chunker = NPChunker()
chunker.train()


with open('../data/posAdj.csv', 'r') as csvfile:
    spamwriter = csv.reader(csvfile)
    pos_words = list(spamwriter)

with open('../data/negAdj.csv', 'r') as csvfile:
    spamwriter = csv.reader(csvfile)
    neg_words = list(spamwriter)

pos_words = [word[0] for word in pos_words]
neg_words = [word[0] for word in neg_words]

posSeed_list = {key:True for key in pos_words}
negSeed_list = {key:False for key in neg_words}

# print(posSeed_list)
# print(negSeed_list)

posSeed_list.update(negSeed_list)
seed_list = posSeed_list

checkWords = list()
with open('../data/vocabulary.csv','r') as vocab:
    spamwriter = csv.reader(vocab)
    checkWords = list(spamwriter)

checkWords = [word[0] for word in checkWords]

# checkWords = checkWords
print(checkWords)

def findLemmas(adj):
    synonyms = []
    antonyms = []
    word = Word(adj)
    for syn in word.synsets[:]:
    # for syn in list(wn.senti_synsets(adj)):
        for l in syn.lemmas():
        # for l in syn.synset.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    return synonyms,antonyms



def findOrientation(adjList,seedList):
    orientations = dict()

    notDone = list()
    for adjective in adjList:
        if adjective in seedList:
            continue
        synonyms,antonyms = findLemmas(adjective)
        check = False
        # notDone = list()

        for synonym in synonyms:
            if synonym in seedList:
                orient = seedList[synonym]
                seedList[adjective] = orient
                # print(adjective + "," + str(orient) + ",matches:" + synonym)
                check = True
                break

        if check:
            continue
        for antonym in antonyms:
            if antonym in seedList:
                orient = not seedList[antonym]
                seedList[adjective] = orient
                # print(adjective + "," + str(orient) + ",matches:" + antonym)
                check = True
                break
        if not check:
            notDone.append(adjective)

    return notDone,seedList

def OrientationSearch(adjList,seedList):
    size1 = 0
    size2 = 1
    while size1 != size2:
        size1 = len(seedList)
        adjList,seedList = findOrientation(adjList,seedList)
        # print(adjList)
        size2 = len(seedList)
        print(str(size1) + "," + str(size2))

    print(adjList)
    # print(seedList)


OrientationSearch(checkWords,seed_list)

finalPosWords = [word for word in seed_list.keys() if seed_list[word] is True]
finalNegWords = [word for word in seed_list.keys() if seed_list[word] is False]

with open('../data/finalPosWords.csv','w') as csvfile:
    spamwriter = csv.writer(csvfile , delimiter='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(finalPosWords)


with open('../data/finalNegWords.csv','w') as csvfile:
    spamwriter = csv.writer(csvfile , delimiter='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(finalNegWords)

# print(findLemmas('horror'))
# print(set(synonyms))
# print(set(antonyms))
# word = Word("crisp",pos_tag="ADJ")
# print(word.synsets[:5])
# w = L('crisp.a.1').antonyms()
# print(w)
# print(wn.synsets('tasty',pos=wn.ADJ))