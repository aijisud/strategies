#!/usr/bin/env python

import subprocess
from os import path
import time

dbhost = "127.0.0.1:27017"

export_path = "D:\mongo\export"
dump_path = "D:\mongo\dump"


def mongoexport(db_name, collection_name):
    date = time.strftime("%Y%m%d")
    csv_file_name = "%s.%s.%s.csv" % (db_name, collection_name, date)
    json_file_name = "%s.%s.%s.json" % (db_name, collection_name, date)

    csv = path.join(export_path, csv_file_name)
    json = path.join(export_path, json_file_name)

    cmd = "mongoexport -h %s -d %s -c %s -o %s" % (dbhost, db_name, collection_name, csv)
    status, output = subprocess.getstatusoutput(cmd)
    print(status, output)

    cmd = "mongoexport -h %s -d %s -c %s -o %s" % (dbhost, db_name, collection_name, json)
    status, output = subprocess.getstatusoutput(cmd)
    print(status, output)


def mongoimport(db_name, collection_name):
    pass


def mongodump(db_name):
    date = time.strftime("%Y%m%d")
    cmd = "mongodump -h %s -d %s -o %s" % (dbhost, db_name, dump_path)
    status, output = subprocess.getstatusoutput(cmd)
    print(status, output)


def mongorestore(db_name):
    pass


if __name__ == '__main__':
    """
    mongoexport("stock", "stocklist")
    mongoexport("stock", "thsstocklist")
    mongoexport("stock", "tusharestocklist")
    """
    mongodump("stock")


#end
