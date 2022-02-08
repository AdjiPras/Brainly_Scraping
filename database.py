from pymongo import MongoClient

class dbBrainly(object):
    client = MongoClient()

    def __init__(self, db_name):
        self.database = db_name

    def insert_url(self, collection, url):
        db  = self.client[self.database]
        db[collection].insert_one({'url':url})

    def get_all_urls(self, collection):
        db = self.client[self.database]
        collection = db[collection]
        result = collection.find()
        return result

    def insert_info(self, collection, data):
        db = self.client[self.database]
        db[collection].insert_one(data)
    
