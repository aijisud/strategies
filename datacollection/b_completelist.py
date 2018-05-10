# -*- coding: utf-8 -*-

import pymongo
import json
import tushare as ts
from os import path

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)

collection = client["stock"]["stocklist"]
invalid = [ "300454", "603259", "603045", "601990", "603013", "300745", "300742", "601206", "603302", "300728", "603587", "300646" ]


def update_market_and_valid():
    result = collection.update_many( {}, { "$set": {"valid": True, "market": "SZ"} } )
    print(result.matched_count, result.modified_count)

    result = collection.update_many( {"code": { "$regex" : "^60...." } }, { "$set": {"market": "SH"} } )
    print(result.matched_count, result.modified_count)


def update_some_valid_false():
    result = collection.update_many( {"code": { "$in" : invalid } }, { "$set": {"valid": False} } )
    print(result.matched_count, result.modified_count)


if __name__ == '__main__':
    #update_market_and_valid()
    update_some_valid_false()

#end
