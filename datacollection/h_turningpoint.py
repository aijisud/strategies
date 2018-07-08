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
    if "trend" in client["analysis"].collection_names():
        client["analysis"]["trend"].rename("trend" + time.strftime("%Y%m%d%H%M%S"))
        print("moved...")
    else:
        print("none to move...")


def delete_history():
    collection_ma20 = client["analysis"]["trend"]
    delete_result = collection_ma20.delete_many({})
    print("deleted...%d" % delete_result.deleted_count)


def get_ma20_of_one(trend_data):
    data_to_be_inserted = []

    turningpoint = -1
    if trend_data[0]["trend"] != "up":
        turningpoint = -1

    index = 0
    uplimit = {}

    latest_days_list = [5, 10, 20, 30, 60]

    for temp in latest_days_list:
        uplimit["latest" + str(temp) ] = 0

    for k in trend_data:
        if k["uplimit"] and index <= max(latest_days_list) :
            for temp in latest_days_list:
                if index < temp:
                    uplimit["latest" + str(temp)] = uplimit["latest" + str(temp)] + 1

        k_trend = trend_data[index: index + 2]
        if len(k_trend) == 1:
            pass
        elif turningpoint == 0 or turningpoint > 0:
            pass
        elif k_trend[0]["trend"] == "down":
            pass
        elif k_trend[0]["trend"] == "up" and k_trend[1]["trend"] == "down":
            turningpoint = index
        elif k_trend[0]["trend"] == "up" and k_trend[1]["trend"] == "up":
            pass

        index = index + 1

    dict_to_be_inserted = { "code": trend_data[0]["code"], "date": trend_data[0]["date"], "turningpoint": turningpoint, "uplimit": uplimit }
    data_to_be_inserted.append(dict_to_be_inserted)

    return data_to_be_inserted


def bulk_insert_ma20(data_to_be_inserted):
    collection_ma20 = client["analysis"]["trend"]
    result = collection_ma20.insert_many(data_to_be_inserted)
    print("inserted %d..." % len(result.inserted_ids) )


def bulk_get_ma20_and_insert():
    all = query_all_stock_list()
    slice = [ all[i:i+300] for i in range(0, len(all), 300) ]

    print("start loop pool...")

    for i in range(len(slice)):
        code_list = slice[i]

        collection = client["analysis"]["turningpoint"]

        dbdata = collection.find({"code": { "$in": code_list } }).sort("date", pymongo.DESCENDING)
        k_data = list(dbdata)
        index = 0

        k_data_group = []
        for code in code_list:
            k_data_one = [ item for item in k_data if item["code"] == code ]
            if k_data_one:
                #如果不为空，插入
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
