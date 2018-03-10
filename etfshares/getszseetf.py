# -*- coding: utf-8 -*-

import requests
from urllib.request import urlretrieve
import os
import time


cwd = os.getcwd()
today = time.strftime("%Y%m%d")

DIR = "data"
URL = "http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1945&ENCODE=1&TABKEY=tab1"
szse_file = today + "_szse_" + "ETF列表.xlsx"

file_name = os.path.join(cwd, DIR, szse_file)


flag_not_get = True
flag_not_get = not os.path.exists(file_name)

max_error = 20
i = 0
sleep_time = 60
while flag_not_get:
    print(i)

    if i >= max_error:
        print("break")
        break
    try:
        urlretrieve(URL, file_name)
        print("got")
    except Exception as e:
        print("exception")
        flag_not_get = True
    else:
        print("else ok")
        break

    time.sleep(sleep_time)
    sleep_time = sleep_time + 60


if os.path.exists(file_name):
    print("got")
    exit(0)
else:
    exit(1)


#end
