# -*- coding: utf-8 -*-

import pymongo

MONGO_URL = "127.0.0.1:27017"

class dbclient(pymongo.MongoClient):

    def __init__(self, url = MONGO_URL):
        pymongo.MongoClient.__init__(self, url)

    def get_all_collections(self, db_name):
        return self[db_name].collection_names()

    def exists(self, db_name, collection_name):
        return collection_name in self[db_name].collection_names()

    def rename(self, db_name, collection_name, newcollection_name):
        if self.exists(db_name, collection_name):
            self[db_name][collection_name].rename(newcollection_name)
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
    c = dbclient()
    cc = c["analysis"]["turningpoint"]
    #print(c.get_all_collections("analysis"))

    result = cc.delete_many({"trend": None})
    print(result.deleted_count)

#end
