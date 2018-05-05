# -*- coding: utf-8 -*-

import pymongo
import sys
import json
import tushare as ts

MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'stock',
    'username': None,
    'password': None
}


class MongoConn(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
        self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
        self.username=MONGODB_CONFIG['username']
        self.password=MONGODB_CONFIG['password']
        if self.username and self.password:
            self.connected = self.db.authenticate(self.username, self.password)
        else:
            self.connected = True

    def disconnect(self):
        self.connected = False
        self.db.logout()


def tushare_to_mongo():
    conn = pymongo.Connection('127.0.0.1', port=27017)
    df_index = ts.get_tick_data('600848',date='2014-12-22')
    df = df_index.reset_index()
    conn.db.tickdata.insert(json.loads(df.to_json(orient='records')))


def main_test():
    # mongodb服务的地址和端口号

    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    #连接到数据库myDatabase
    DATABASE = "stocks"
    db = client[DATABASE]

    #连接到集合(表):myDatabase.myCollection
    COLLECTION = "stocks"
    db_coll = db[COLLECTION]

    insert_record = {"monitor_list": [{"stock_code": "600460", "stock_name": "士兰微"}, {"stock_code": "600088", "stock_name": "中视传媒"}]}
    db_coll.insert_one(insert_record)

def df_to_mongo(df, collection):
    df_no_index = df.reset_index()
    result = collection.insert(json.loads(df_no_index.to_json(orient='records')))
    return result

if __name__ == '__main__':

    mongo_url = "127.0.0.1:27017"
    conn = pymongo.MongoClient(mongo_url)
    df = ts.get_stock_basics()
    print(df_to_mongo(df, conn.stock.tusharestocklist))


#end
