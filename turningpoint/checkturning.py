# -*- coding: utf-8 -*-

import tushare as ts

import time
from datetime import datetime, date, timedelta

trend = 5

"""
FIRST_DAY = datetime.strptime("20180101", "%Y%m%d")
FIRST_DAY - timedelta(30)
"""
today = time.strftime("%Y-%m-%d")

def get_recent_days():
    ts.get_k_data('000001', index = True, start = '2018-01-01', end = today)
    return []


def get_stocks():
    rows = []
    with open('stocks.txt', encoding="utf-8-sig") as f:
        lines = f.readlines()
        for data in lines:
            rows.append(data[2:8].rstrip("\n"))
    count = len(rows)
    return rows


def get_ma20(stock_code):
    df = ts.get_hist_data(stock_code, start = '2018-01-01', end = today)
    return df



def check_today_turning(stock_code):
    #连续trend的向下
    get_ma20(stock_code)

    return True


def check_dense():
    return True


def loop_process():
    for stock_code in get_stocks():
        #print(stock_code)
        df = get_ma20(stock_code)
        df_ma = df.iloc[0:6][['ma5', 'ma10', 'ma20']]
        print(df_ma)
        return

if __name__ == '__main__':

    loop_process()
    #print(check_today_turning(""))




#end
