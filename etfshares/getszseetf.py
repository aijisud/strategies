# -*- coding: utf-8 -*-

import requests
from urllib.request import urlretrieve
import os
import time

today = time.strftime("%Y%m%d")

URL = "http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1945&ENCODE=1&TABKEY=tab1"
DIR = "data"
sse_file = today + "_sse_" + "ETF列表.xlsx"

file_name = os.path.join(DIR, sse_file)

urlretrieve(URL, file_name)



#end
