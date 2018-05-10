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


def move_history():
    if "tusharekdata" in client["stock"].collection_names():
        client["stock"]["tusharekdata"].rename("tusharekdata" + time.strftime("%Y%m%d%H%M%S"))
        print("moved...")
    else:
        print("none to move...")


def delete_last_data():
    collection = client["stock"]["tusharekdata"]
    result = collection.delete_many({})
    print("deleted...%d" % result.deleted_count)


def insert_tushare_data_of_one(stock_code):
    collection = client["stock"]["tusharekdata"]

    #get full time data
    #df = ts.get_k_data(stock_code, start = FIRST_DAY, end = today)

    #get recent data
    df = ts.get_k_data(stock_code)

    if df is None or len(df) == 0:
        print("%s: %d" % (stock_code, 0))
        return
    #df["code"] = stock_code
    data = json.loads(df.reset_index().to_json(orient='records'))

    result = collection.insert_many(data)
    print("%s: %d" % (stock_code, len(result.inserted_ids)))


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

    for i in range(8):
        print(i)
        l = get_stock_list_lack()
        if len(l) == 0:
            print("len is 0")
        pool = Pool()
        pool.map(insert_tushare_data_of_one, l[:512])
        pool.close()
        pool.join()
        print("sleeping...")
        time.sleep(20)

    print("all done...")


if __name__ == '__main__':

    print(time.time())
    move_history()
    print(time.time())
    bulk_insert_tushare_data()
    print(time.time())
    print("all done...")


#end
