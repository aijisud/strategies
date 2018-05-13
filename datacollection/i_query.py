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


def query():

    collection = client["analysis"]["trend20180510230432"]
    #dbdata = collection.find({ "turningpoint": {"$in": [1,2,3,4,5]}, "uplimit.latest20": {"$eq": 2}, "uplimit.latest5": {"$eq": 0} })
    dbdata = collection.find({ "turningpoint": {"$in": [1,2,3,4,5,6,7,8,9]}, "uplimit.latest60": {"$gt": 3}, "uplimit.latest5": {"$eq": 0} })
    data = [ row["code"] for row in dbdata ]
    print(data)
    print(len(data))


if __name__ == '__main__':

    query()
    print("all done...")


#end
