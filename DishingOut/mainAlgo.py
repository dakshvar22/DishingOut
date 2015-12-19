import json
from dishingOut.NPChunking.NPChunker import NPChunker
from dishingOut.SentimentAnalysis.antonymReplacer import AntonymReplacer
import pickle
import time

with open('../data/final_data.json','r') as f:
    data = json.load(f)

chunker = NPChunker()
chunker.train()
replacer = AntonymReplacer()
f = open('../SentimentAnalysis/nb_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

print("Done pre-processing")

def word_feats(words):
    return dict([word,True] for word in words)


start = time.time()
restaurants = data
for restaurant in restaurants:
    dishes = restaurant['dishes']
    restaurant['dishRatings'] = dict()
    print(dishes.keys())
    allChunks = dict()
    for dish in dishes.keys():
        # print(dish)
        pos = 0.0
        neg = 0.0
        count=0
        try:
            reviews = dishes[dish]
            chunks = list()
            for review in reviews:
                tree, terms = chunker.extractChunk(review)
                for opinion in terms:
                    sentence = ' '.join(opinion)
                    if dish in sentence:
                        chunks.append(sentence)
                        if opinion!=[]:
                            count+=1
                            check, words = replacer.NegationCheck(sentence)
                            features = word_feats(words)
                            probab = classifier.prob_classify(features)
                            p = probab.prob('pos')
                            n = probab.prob('neg')
                            if check==True:
                                p,n=n,p
                            pos+=p
                            neg+=n
                        #~ print words, p.prob('pos'), p.prob('neg')
            pos/=count
            neg/=count
            # dishes[dish].append(pos)
            # dishes[dish].append(neg)
            chunks.append(pos)
            chunks.append(neg)
            allChunks[dish] = chunks
            print(pos, neg, dish)

        except:
            print(dish)
            pass
    restaurant['dishRatings']['ChunksWithRatings'] = allChunks

print(time.time()-start)
with open('../data/dish_ratings.json','w') as f:
    json.dump(restaurants,f,indent=2)

