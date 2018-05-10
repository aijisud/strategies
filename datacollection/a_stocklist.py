# -*- coding: utf-8 -*-

import pymongo
import json
import tushare as ts
from os import path

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)


def insert_into_tushare_stock_list():
    collection = client["stock"]["tusharestocklist"]

    df = ts.get_stock_basics()
    data = json.loads(df.reset_index().to_json(orient='records'))
    #print(data)

    result = collection.delete_many({})
    print(result.deleted_count)

    result = collection.insert_many(data)
    print(len(result.inserted_ids))


def insert_into_ths_stock_list():

    data = []
    file = "E:/Table.txt"
    if not path.exists(file):
        print("not exists")
        return
    with open(file, "r", encoding = "gbk") as f:
        lines = f.readlines()
        for line in lines[1:]:
            stock_dict = {}
            if len(line) > 8:
                cols = line.split("\t")
                stock_dict["code"] = cols[0][2:8]
                stock_dict["name"] = cols[1]
                stock_dict["market"] = cols[0][0:2]
                data.append(stock_dict)
    """
    代码		    名称		涨幅%		现价		涨跌		涨速%		主力净量		总手		换手%		量比		所属行业		现手		开盘		昨收		最高		最低		买价		卖价		市盈(动)		市净率		买量		卖量		委比%		振幅%		总金额		均笔额		笔数		手/笔		外盘		内盘		总市值		流通市值		贡献度		净资产收益率
    """

    collection = client["stock"]["thsstocklist"]

    result = collection.delete_many({})
    print(result.deleted_count)

    result = collection.insert_many(data)
    print(len(result.inserted_ids))


def insert_test():

    d = {}
    d["a"] = "b"
    d["c"] = 1.1
    e = {
        "ee": "222",
        "ff": 222
    }

    l = []
    l.append(d)
    l.append(e)
    print(type(d))

    r = client["test"]["collection"].insert_many(l)

    print(r)
    print(type(r.inserted_ids))
    print(len(r.inserted_ids))


def query_stock_list(source = "tushare"):
    collection = client["stock"][source + "stocklist"]
    dbdata = collection.find({})
    data = [ { "code" : row["code"], "name" : row["name"] } for row in dbdata ]
    return data


def union_all_stock_list():
    #tushare is more exact
    d1 = query_stock_list()

    d2 = query_stock_list(source = "ths")

    d3 = [ data for data in d2 if data["code"] not in [ row["code"] for row in d1 ] ]
    d4 = [ data for data in d1 if data["code"] not in [ row["code"] for row in d2 ] ]

    #print(d3)
    d1.extend(d3)
    #print(len(d1))

    """
    print(d4)
    d2.extend(d4)
    print(len(d2))
    exit(0)
    """

    collection = client["stock"]["stocklist"]

    result = collection.delete_many({})
    print(result.deleted_count)

    result = collection.insert_many(d1)
    print(len(result.inserted_ids))


if __name__ == '__main__':
    print("insert_into_tushare_stock_list...")
    insert_into_tushare_stock_list()

    print("insert_into_ths_stock_list...")
    insert_into_ths_stock_list()

    print("union_all_stock_list...")
    union_all_stock_list()


#end
