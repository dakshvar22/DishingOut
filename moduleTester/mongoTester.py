
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['test']
collection = db.get_collection('coll')
print(collection.find_one())