# -*- coding: utf-8 -*-

import pymongo
import json
import tushare as ts
from multiprocessing import Pool, Process

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)


"""
NOT IN USE
db: kdata
"""
def get_tushare_k_data(stock_code):
    collection = client["kdata"][stock_code]

    df = ts.get_hist_data(stock_code)
    if df is None:
        print("0")
        return
    data = json.loads(df.reset_index().to_json(orient='records'))
    #print(data)

    result = collection.delete_many({})
    print(result.deleted_count)

    result = collection.insert_many(data)
    print(len(result.inserted_ids))


def delete_data():
    collection = client["stock"]["tusharedata"]
    result = collection.delete_many({})
    print("deleted...%d" % result.deleted_count)


def get_tushare_data_of_one(stock_code):
    collection = client["stock"]["tusharedata"]
    df = ts.get_hist_data(stock_code)
    if df is None:
        print("%s: %d" % (stock_code, 0))
        return
    df["code"] = stock_code
    data = json.loads(df.reset_index().to_json(orient='records'))

    result = collection.insert_many(data)
    print("%s: %d" % (stock_code, len(result.inserted_ids)))


def get_stock_list_from_db():
    collection = client["stock"]["thsstocklist"]
    results = collection.find({})
    l = [result["code"] for result in results]
    return l


def multiprocessing_in_pool():

    pool = Pool()
    pool.map(get_tushare_data_of_one, get_stock_list_from_db())
    pool.close()
    pool.join()

    print("all done...")


def get_db_all_collections():
    db = client["stock"]
    result = db.collection_names()
    print(result)


def get_stock_list_got():
    collection = client["stock"]["tusharedata"]
    dbdata = collection.aggregate([{ '$group' : {'_id':'$code', 'count':{'$sum':1} } }])
    data = list(dbdata)
    l = [row["_id"] for row in data ]
    return l


if __name__ == '__main__':

    #get_tushare_k_data("600000")
    #get_tushare_data_of_one("002583")

    """
    delete_data()
    multiprocessing_in_pool()
    """
    less = get_stock_list_got()
    more = get_stock_list_from_db()
    c = [item for item in more if item not in less]
    print(c)
    print(len(c))

#end
