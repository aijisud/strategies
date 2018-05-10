# -*- coding: utf-8 -*-

import time
import json
import pymongo
import tushare as ts
from multiprocessing import Pool, Process

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)

FIRST_DAY = "1990-12-19"
today = time.strftime("%Y-%m-%d")


def query_all_stock_list():
    collection = client["stock"]["stocklist"]
    dbdata = collection.find({ "valid": True })
    data = [ row["code"] for row in dbdata ]
    return data


def query_k_data_got_list():
    collection = client["stock"]["tusharekdata"]
    dbdata = collection.aggregate([{ '$group' : {'_id':'$code', 'count':{'$sum':1} } }])
    data = list(dbdata)
    l = [row["_id"] for row in data ]
    return l


def get_stock_list_lack():
    less = query_k_data_got_list()
    more = query_all_stock_list()
    c = [item for item in more if item not in less]
    return c


def bulk_insert_tushare_data():

    print("deleting...")
    delete_last_data()
    print("deleted...")

    for i in range(8):
        print(i)
        l = get_stock_list_lack()
        pool = Pool()
        pool.map(insert_tushare_data_of_one, l[:256])
        pool.close()
        pool.join()
        print("sleeping...")
        time.sleep(60)

    print("all done...")


if __name__ == '__main__':

    #bulk_insert_tushare_data()
    print(get_stock_list_lack())


#end
