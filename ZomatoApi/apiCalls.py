__author__ = 'daksh'

import requests as re

class apiCalls:
    def __init__(self):
        self.headers = {
                'X-Zomato-API-Key': "7749b19667964b87a3efc739e254ada2",
                'cache-control': "no-cache",
                "user-agent" : "myapp",
                'postman-token': "58b1afdb-8a80-b361-bfc8-4949a8215857"
        }
        self.url = "https://api.zomato.com/v1"

    def getListOfRestaurants(self,city_id,offset):

        url = self.url+'/search.json'
        querystring = {"city_id":str(city_id),"count":"50","start":str(offset)}
        response = re.request("GET", url, headers=self.headers, params=querystring)

        return(response.json())

    def getReviews(self,id):

        url = self.url + '/reviews.json/'+str(id)+'/user'
        start = 0
        flag = True
        reviews = list()
        while(True):

            querystring = {"start":start,"count":"50"}
            response = re.request("GET", url, headers=self.headers, params=querystring).json()
            count = response['reviewsShown']
            if(count == 0):
                break

            userReviews = response['userReviews']
            reviewsSet = [review['review'] for review in userReviews]

            reviews += reviewsSet
            start = start + count

        print(len(reviews))
        # print(reviews[0])
        # print(reviews[1])
        return reviews

if __name__ == '__main__':
    zomato = apiCalls()
    print(zomato.getReviews(58273))