__author__ = 'daksh'
import time
from dishingOut.Database.database import MongoOperator as mongo
from dishingOut.NPChunking.NPChunker import NPChunker
import csv
import json

chunker = NPChunker()
chunker.train()


''' Get all test adjectives : Unfiltered. Around 1 lakh adjectives. Contains a lot of non adjectives'''
# database = mongo('DishingOut')
# database.setUpConnection()
# database.setUpCollection('reviews')

# restaurants = database.getAll()
restaurants = None
with open('../data/restaurants.json') as data_file:
	restaurants = json.load(data_file)
restaurants = restaurants[2000:]
start = time.time()
# for restaurant in restaurants:
#     for review in restaurant['userReviews']:
#         text = review['reviewText']
#         sentences = chunker.split(text)
#         for sent in sentences:
#             tree,terms = chunker.extractChunk(sent)
#             print(tree)

vocabulary = list()
with open('../data/vocabulary.csv', 'r') as csvfile:
    spamwriter = csv.reader(csvfile)
    vocabulary = list(spamwriter)

vocabulary = [word for [word] in vocabulary]

count = 0
reviewCount = 0
for restaurant in restaurants:
    try:
        resId = restaurant['resId']
        count = count + 1
        print("count " + str(count))
        print('Doing for '+resId)
        for review in restaurant['userReviews']:
            text = review['reviewText']
            reviewCount +=1
            print('Review number' + str(reviewCount))
            adjectives = chunker.getAdjectives(text)
            print('Restaurants done' + str(count))
            if adjectives:
                for (adj,tag) in adjectives:
                    # print(adj.lower())
                    if adj.lower() not in vocabulary:
                        vocabulary.append(adj.lower())
    except:
        pass


print(time.time()-start)
print(len(vocabulary))
with open('../data/vocabulary.csv', 'a', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(vocabulary)

# print(len(restaurants))

# chunker.train()
# tree,terms = chunker.extractChunk("Dosa was good")
# print(chunker.getAdjetives("Dosa was good"))

