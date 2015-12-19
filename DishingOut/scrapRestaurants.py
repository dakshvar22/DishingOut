__author__ = 'daksh'

from dishingOut.Database.database import MongoOperator as mongo
from dishingOut.ZomatoApi.apiCalls import apiCalls as api

database = mongo('DishingOut')
database.setUpConnection()
zomato = api()

wanted_keys = ['id','name','address','latitude','longitude','cuisines','cost_for_two','rating_aggregate']

database.setUpCollection('restaurants')
count=0
total = 0
for i in range(0,155):
    resp = zomato.getListOfRestaurants(4,50*i)['results']

    listOfRes = list()
    count = 0
    for i in resp:
        restaurant = i['result']
        resDB = {key:restaurant[key] for key in wanted_keys }
        listOfRes.append(resDB)
        count = count+1
        print(str(count) + 'appended')

    # print(resDB)

    database.insertMany(listOfRes)
    total = total+50
    print(str(total) + 'inserted')

# print(len(database.getAll()))
count = 0
for record in database.getAll():
    count += 1
    print(record)

print(count)
# print(resp['restaurants'][0]['restaurant']['name'])
# print(resp['restaurants'][19]['restaurant']['id'])
# print(resp['restaurants'][19]['restaurant']['location'])
# print(resp['restaurants'][19]['restaurant']['cuisines'])
# print(resp['restaurants'][19]['restaurant']['average_cost_for_two'])
# print(resp['restaurants'][19]['restaurant']['user_rating'])

# print(resp)