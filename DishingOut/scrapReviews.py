__author__ = 'daksh'

from dishingOut.Database.database import MongoOperator as mongo
from dishingOut.ZomatoApi.apiCalls import apiCalls as api

database = mongo('DishingOut')
database.setUpConnection()
zomato = api()

database.setUpCollection('restaurants')
resIds = list()
for record in database.getAll():
    resIds.append(record['id'])

reviewsDone = list()
database.setUpCollection('reviews')
for record in database.getAll():
    reviewsDone.append(record['resId'])

count = 0
for id in resIds:
    print('Doing for' + str(id))
    if(id in reviewsDone):
        print('already done')
        continue
    reviews = zomato.getReviews(id)
    document = dict()
    document['resId'] = id
    document['numberOfReviews'] = len(reviews)
    document['userReviews'] = reviews

    database.insertOne(document)
    # count+=1
    # if count == 2:
    #     break

database.closeConnection()

print(resIds.index("50870"))
print(len(resIds))