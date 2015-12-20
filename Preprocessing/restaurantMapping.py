__author__ = 'pawan'
from dishingOut.ZomatoApi.apiCalls import apiCalls
import json

zomato = apiCalls()

with open('../data/dish_ratings.json','r') as f:
    data = json.load(f)

finaldata = dict()
i=0

for restaurant in data:
    try:
        print i
        i+=1
        restaurantName = zomato.getRestaurantFromId(restaurant['resId'])
        finaldata[restaurant['resId']] = restaurantName
    except:
        pass

with open('../data/restaurantMapping.json','w') as f:
    json.dump(finaldata, f, indent=2)
