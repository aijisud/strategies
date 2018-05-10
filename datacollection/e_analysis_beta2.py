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


def delete_history():
    collection_ma20 = client["analysis"]["ma20"]
    delete_result = collection_ma20.delete_many({})
    print("deleted...%d" % delete_result.deleted_count)


def get_ma20_of_one(code):

    query_client = pymongo.MongoClient(mongo_url)
    collection = query_client["stock"]["tusharekdata"]

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

    return data_to_be_inserted


def bulk_insert_ma20(data_to_be_inserted):
    insert_client = pymongo.MongoClient(mongo_url)
    collection_ma20 = insert_client["analysis"]["ma20"]
    result = collection_ma20.insert_many(data_to_be_inserted)
    print("inserted %d..." % len(result.inserted_ids) )


def bulk_get_ma20_and_insert():
    all = query_all_stock_list()
    slice = [ all[i:i+300] for i in range(0, len(all), 300) ]

    print("start loop pool...")

    for i in range(len(slice)):
        pool = Pool()
        result = pool.map(get_ma20_of_one, slice[i])
        pool.close()
        pool.join()

        data = []
        for r in result:
            data.extend(r)
        print(len(slice))
        print(len(data))
        bulk_insert_ma20(data)
        print("insert %d done..." % i)
    print("all done...")


if __name__ == '__main__':
    print(time.time())
    #delete_history()
    print(time.time())
    bulk_get_ma20_and_insert()
    print(time.time())
    print("all done...")


#end
