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

    collection = client["analysis"]["trend"]

    print("****************************************")
    print("拐点2天内，涨停最近20天大于1个：")
    dbdata = collection.find({ "turningpoint": {"$in": [1,2]}, "uplimit.latest20": {"$gt": 1} })
    data = [ row["code"] for row in dbdata ]
    print(data)
    print("****************************************")

    print("拐点5天内，涨停最近20天大于1个，最近5天没有：")
    dbdata = collection.find({ "turningpoint": {"$in": [1,2,3,4,5]}, "uplimit.latest20": {"$gt": 1}, "uplimit.latest5": {"$eq": 0} })
    data = [ row["code"] for row in dbdata ]
    print(data)
    print("****************************************")

    print("拐点5天内，涨停最近20天大于1个：")
    dbdata = collection.find({ "turningpoint": {"$in": [1,2,3,4,5]}, "uplimit.latest20": {"$gt": 1}, "uplimit.latest5": {"$eq": 0} })
    data = [ row["code"] for row in dbdata ]
    print(data)
    print("****************************************")

    print("拐点10天内，涨停最近60天大于2个，最近20天大于1个：")
    dbdata = collection.find({ "turningpoint": {"$in": [1,2,3,4,5,6,7,8,9,10]}, "uplimit.latest60": {"$gt": 2}, "uplimit.latest20": {"$gt": 1} })
    data = [ row["code"] for row in dbdata ]
    print(data)
    print("****************************************")


if __name__ == '__main__':

    query()
    print("all done...")


#end
