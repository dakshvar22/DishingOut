__author__ = 'daksh'

import requests as re
import json

url = "https://developers.zomato.com/api/v2.1/search"

querystring = {"entity_id":"4","entity_type":"city","count":"20"}

headers = {
    'user_key': "5aaccd440d555c8152be2d034a518811",
    'cache-control': "no-cache",
    "user-agent" : "myapp",
    'postman-token': "58b1afdb-8a80-b361-bfc8-4949a8215857"
    }

response = re.request("GET", url, headers=headers, params=querystring)

# response = re.get(url="http://www.google.com")
print(response.text)
# parsed = json.loads(response.text)
# print(json.dumps(parsed,indent=4))
print(querystring['count'])
# import http.client
#
# conn = http.client.HTTPSConnection("developers.zomato.com")
#
# headers = {
#     'user_key': "5aaccd440d555c8152be2d034a518811",
#     'cache-control': "no-cache",
#     'postman-token': "6b4ced6d-f05a-23fd-e6d6-bdda6f2d4791"
#     }
#
# conn.request("GET", "/api/v2.1/search?entity_id=4&entity_type=city&count=20", headers=headers)
#
# res = conn.getresponse()
# data = res.read()
#
# print(data.decode("utf-8"))