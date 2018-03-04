# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd

code='601988'
start_end = '2017-09-15'

s = 'none'

try:
    df = ts.get_k_data(code, start=start_end, end=start_end)
except Exception as e:
    s = str(e)

for index, row in df.iterrows():
    s = "%s,%s,%s,%s,%s,%s" % (str(row['date']), str(row['code']),
        str(row['open']), str(row['close']), str(row['high']), str(row['low']))

with open('a.log', 'w') as f:
    f.write(s)

#end
