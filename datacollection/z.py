# -*- coding: utf-8 -*-

import pymongo

MONGO_URL = "127.0.0.1:27017"

class z(pymongo.MongoClient):

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


if __name__ == '__main__':
    c = z()
    cc = c["analysis"]["turningpoint"]
    #print(c.get_all_collections("analysis"))

    result = cc.delete_many({"trend": None})
    print(result.deleted_count)

#end
