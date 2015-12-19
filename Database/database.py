__author__ = 'daksh'

from pymongo import MongoClient

class MongoOperator():
    def __init__(self,db):
        self.dbName = db

    def setUpConnection(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.dbName]

    def setUpCollection(self,collName):

        if(collName in self.db.collection_names()):
            self.collection = self.db.get_collection(collName)
        else:
            self.db.create_collection(collName)
            self.collection = self.db.get_collection(collName)

    def getOne(self):
        print(self.collection.find_one())

    def getAll(self):
        return self.collection.find({})

    def insertOne(self,res):
        self.collection.insert_one(res)

    def insertMany(self,listofRes):
        self.collection.insert_many(listofRes)

    def closeConnection(self):
        self.client.close()


if __name__ == '__main__':
    mongo = MongoOperator('DishingOut')
    mongo.setUpConnection()
    mongo.setUpCollection('reviews')

    reviews = mongo.getAll()
    print(reviews[20])
