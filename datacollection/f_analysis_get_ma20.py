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


def move_history():
    if "ma20" in client["analysis"].collection_names():
        client["analysis"]["ma20"].rename("ma20" + time.strftime("%Y%m%d%H%M%S"))
        print("moved...")
    else:
        print("none to move...")


def delete_history():
    collection_ma20 = client["analysis"]["ma20"]
    delete_result = collection_ma20.delete_many({})
    print("deleted...%d" % delete_result.deleted_count)


def get_ma20_of_one(k_data):
    data_to_be_inserted = []
    k_list = [ k["close"] for k in k_data ]
    index = 0
    for k in k_data:
        kclose = k_list[index: index + 20]
        ma20 = sum(kclose) / len(kclose)
        #print(ma20)
        dict_to_be_inserted = { "code": k["code"], "date": k["date"], "close": k["close"],"ma20": float("%.4f" % ma20) }
        data_to_be_inserted.append(dict_to_be_inserted)
        index = index + 1

    return data_to_be_inserted


def get_ma20_of_slice(k_data):
    pass


def bulk_insert_ma20(data_to_be_inserted):
    collection_ma20 = client["analysis"]["ma20"]
    result = collection_ma20.insert_many(data_to_be_inserted)
    print("inserted %d..." % len(result.inserted_ids) )


def bulk_get_ma20_and_insert():
    all = query_all_stock_list()
    slice = [ all[i:i+300] for i in range(0, len(all), 300) ]

    print("start loop pool...")

    for i in range(len(slice)):
        code_list = slice[i]

        collection = client["stock"]["tusharekdata"]

        dbdata = collection.find({"code": { "$in": code_list } }).sort("date", pymongo.DESCENDING)
        k_data = list(dbdata)
        index = 0

        k_data_group = []
        for code in code_list:
            k_data_one = [ item for item in k_data if item["code"] == code ]
            k_data_group.append(k_data_one)

        pool = Pool()
        result = pool.map(get_ma20_of_one, k_data_group)
        pool.close()
        pool.join()

        """
        pool = Pool()
        result = pool.map(get_ma20_of_slice, slice[i])
        pool.close()
        pool.join()
        """
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
    move_history()
    print(time.time())
    bulk_get_ma20_and_insert()
    print(time.time())
    print("all done...")


#end
