# -*- coding: utf-8 -*-

import pymongo


class y():

    MONGO_URL = "127.0.0.1:27017"

    def __init__(self):
        self.client = pymongo.MongoClient(self.MONGO_URL)

    def client():
        return self.client

    def get_all_collections(self, db_name):
        return self.client[db_name].collection_names()

    def exists(self, db_name, collection_name):
        return collection_name in self.client[db_name].collection_names()

    def rename(self, db_name, collection_name, newcollection_name):
        if self.exists(db_name, collection_name):
            self.client[db_name][collection_name].rename(newcollection_name)
            return True
        return False

    def clone(self, db_name, collection_name, newcollection_name):
        if self.exists(db_name, collection_name):
            #self.client[db_name][collection_name].rename(newcollection_name)
            old = self.client[db_name][collection_name]
            data = old.find({})
            new = self.client[db_name][newcollection_name]
            result = new.insert_many(data)
            return True
        return False


if __name__ == '__main__':
    c = y()
    c.clone("", "", "")

    #print(c.rename("analysis", "ma20", "ma20"))


#end
