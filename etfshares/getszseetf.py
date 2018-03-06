# -*- coding: utf-8 -*-

import requests
from urllib.request import urlretrieve
import os
import time


cwd = os.getcwd()
today = time.strftime("%Y%m%d")

DIR = "data"
URL = "http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1945&ENCODE=1&TABKEY=tab1"
sse_file = today + "_szse_" + "ETF列表.xlsx"

file_name = os.path.join(cwd, DIR, sse_file)

urlretrieve(URL, file_name)



#end
