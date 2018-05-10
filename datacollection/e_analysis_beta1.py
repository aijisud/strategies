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
    collection = client["stock"]["tusharekdata"]
    collection_ma20 = client["analysis"]["ma20"]

    dbdata = collection.find({"code": code}).sort("date", pymongo.DESCENDING)
    k_data = list(dbdata)
    data_to_be_inserted = []
    index = 0
    k_list = [ k["close"] for k in k_data ]
    for k in k_data:
        kclose = k_list[index: index + 20]
        ma20 = sum(kclose) / len(kclose)
        #print(ma20)
        dict_to_be_inserted = { "code": code, "date": k["date"], "ma20": "%.4f" % ma20 }
        data_to_be_inserted.append(dict_to_be_inserted)
        index = index + 1

    result = collection_ma20.insert_many(data_to_be_inserted)
    print("%s inserted %d..." % (code, len(result.inserted_ids)))


def bulk_get_ma20_and_insert():
    collection = client["stock"]["tusharekdata"]
    collection_ma20 = client["analysis"]["ma20"]

    #delete_result = collection_ma20.delete_many({})
    #print("deleted...%d" % delete_result.deleted_count)

    pool = Pool()
    pool.map(get_ma20_and_insert_of_one, query_all_stock_list())
    pool.close()
    pool.join()


if __name__ == '__main__':
    print(time.time())
    bulk_get_ma20_and_insert()
    print(time.time())
    print("all done...")


#end
