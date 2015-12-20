__author__ = 'pawan' # Started using PyCharm

from dishingOut.ZomatoApi.apiCalls import apiCalls
import json

zomato = apiCalls()

with open('../data/dish_ratings.json','r') as f:
    data = json.load(f)

with open('../data/restaurantMapping.json','r') as f:
    restaurantMapping = json.load(f)

# print restaurantMapping
support = 3
finaldata = dict()
i=0
for restaurant in data:
    dishRatings = restaurant['dishRatings']['ChunksWithRatings']
    try:
        restaurantName = restaurantMapping[restaurant['resId']]
    except:
        try:
            restaurantName = zomato.getRestaurantFromId(restaurant['resId'])
        except:
            continue
    ratingList = list()

    for dish in dishRatings:
        # Ensures support. +2 is for including the positive and negative percentages.
        if len(dishRatings[dish])>=5:
            rating = (dish, dishRatings[dish][-2], dishRatings[dish][:-2])
            ratingList.append(rating)
    ratingList.sort(key=lambda x:x[1], reverse=True)

    finaldata[restaurantName]=ratingList

with open('../data/dishReviews.json', 'w') as f:
    json.dump(finaldata, f, indent=2)
