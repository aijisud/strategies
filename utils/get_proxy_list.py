# -*- coding: utf-8 -*-

import time
import requests
import pymongo
from datetime import datetime

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)


def delete_history():
    time_now = datetime.now()
    result = client["toolbox"]["proxy"].delete_many({ "inserted_time": {"$lt": time_now},  })
    print(result.deleted_count)


def get_proxy_list():
    ss = requests.Session()
    proxy_list = []
    result = ss.get("https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list")
    #return result.text
    for i in result.text.split("\n"):
        if i.strip() != "":
            d = eval(i)
            d["inserted_time"] = datetime.now()
            d["used"] = False
            proxy_list.append(d)
    return proxy_list


def insert_into_db(proxy_list):
    mongo_url = "127.0.0.1:27017"
    client = pymongo.MongoClient(mongo_url)
    result = client["toolbox"]["proxy"].insert_many(proxy_list)
    print(len(result.inserted_ids))
    #result = client["toolbox"]["proxy"].update_many({}, {"$set": {"used_time": time.strftime("%Y%m%d%H%M%S") }})
    #print(result.matched_count, result.modified_count)

if __name__ == '__main__':
    while True:
        print("deleting...")
        delete_history()
        print("inserting...")
        insert_into_db(get_proxy_list())
        exit(0)
        print("sleeping...")
        time.sleep( 15 * 60 )


#end
