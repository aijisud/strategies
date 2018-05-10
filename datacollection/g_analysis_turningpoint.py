# -*- coding: utf-8 -*-

import time
import json
from decimal import *
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
    if "turningpoint" in client["analysis"].collection_names():
        client["analysis"]["turningpoint"].rename("turningpoint" + time.strftime("%Y%m%d%H%M%S"))
        print("moved...")
    else:
        print("none to move...")


def delete_history():
    collection_ma20 = client["analysis"]["turningpoint"]
    delete_result = collection_ma20.delete_many({})
    print("deleted...%d" % delete_result.deleted_count)


def check_uplimit(close_list):
    if len(close_list) != 2:
        return False
    up_limit_coefficient = 1.1

    close = close_list[0]
    last_close = close_list[1]
    return float(Decimal(str(last_close * up_limit_coefficient)).quantize(Decimal('1.00'), ROUND_HALF_EVEN)) == close


"""
print(check_uplimit([6.88,6.25]))
print(check_uplimit([5.25,4.77]))
print(check_uplimit([7.22,6.56]))
print(check_uplimit([8.21,7.46]))
print(check_uplimit([11.29,10.26]))
"""


def get_ma20_of_one(k_data):
    data_to_be_inserted = []
    k_list = [ k["ma20"] for k in k_data ]
    k_close = [ k["close"] for k in k_data ]
    index = 0
    for k in k_data:
        ma20_2days = k_list[index: index + 2]
        close_2days = k_close[index: index + 2]

        trend = "up" if len(ma20_2days) == 1 else "up" if ma20_2days[0] >= ma20_2days[1] else "down"
        uplimit = check_uplimit(close_2days)

        dict_to_be_inserted = { "code": k["code"], "date": k["date"], "ma20": k["ma20"], "trend": trend, "uplimit": uplimit }
        data_to_be_inserted.append(dict_to_be_inserted)
        index = index + 1

    return data_to_be_inserted


def get_ma20_of_slice(k_data):
    pass


def bulk_insert_ma20(data_to_be_inserted):
    collection_ma20 = client["analysis"]["turningpoint"]
    result = collection_ma20.insert_many(data_to_be_inserted)
    print("inserted %d..." % len(result.inserted_ids) )


def bulk_get_ma20_and_insert():
    all = query_all_stock_list()
    slice = [ all[i:i+300] for i in range(0, len(all), 300) ]

    print("start loop pool...")

    for i in range(len(slice)):
        code_list = slice[i]

        collection = client["analysis"]["ma20"]

        dbdata = collection.find({"code": { "$in": code_list } }).sort("date", pymongo.DESCENDING)
        k_data = list(dbdata)
        index = 0

        k_data_group = []
        for code in code_list:
            k_data_one = [ item for item in k_data if item["code"] == code ]
            k_data_group.append(k_data_one)

        #print(get_ma20_of_one(k_data_group[0]))
        #exit()

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
