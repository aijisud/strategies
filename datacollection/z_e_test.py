# -*- coding: utf-8 -*-

import time
import json
import pymongo
import tushare as ts
from multiprocessing import Pool, Process

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)


def query_all_stock_list():
    collection = client["stock"]["stocklist"]
    dbdata = collection.find({ "valid": True })
    data = [ row["code"] for row in dbdata ]
    return data


def get_ma20_and_insert_of_one(code):
    return [ {"code": code, "time": time.time() } ]


def bulk_get_ma20_and_insert():
    collection = client["stock"]["tusharekdata"]
    collection_ma20 = client["analysis"]["ma20"]

    delete_result = collection_ma20.delete_many({})
    print("deleted...%d" % delete_result.deleted_count)

    all = query_all_stock_list()
    for i in range(8):
        print(i)
        pool = Pool()
        result = pool.map(get_ma20_and_insert_of_one, all[0:600])
        pool.close()
        pool.join()



if __name__ == '__main__':
    print(time.time())
    bulk_get_ma20_and_insert()
    print(time.time())
    print("all done...")


#end
