# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import os
from os import path
import time
from datetime import datetime, date, timedelta

TREND = 5

DELTA = 100

today = time.strftime("%Y-%m-%d")
start = datetime.strftime(datetime.now().date() - timedelta(DELTA), "%Y-%m-%d")


cwd = os.getcwd()
data_dir = path.join(cwd, "tusharedata", time.strftime("%Y%m%d"))


def get_stocks():
    rows = []
    with open('stocks.txt', encoding="utf-8-sig") as f:
        lines = f.readlines()
        for data in lines:
            rows.append(data[2:8].rstrip("\n"))
    count = len(rows)
    return rows

list_stocks = get_stocks()


def get_recent_days():
    #not in use
    ts.get_k_data('000001', index = True, start = '2018-01-01', end = today)
    return []


def get_df(stock_code):
    df = ts.get_hist_data(stock_code, start = '2017-12-01', end = today)
    return df


def get_ma20(stock_code):
    #df = ts.get_hist_data(stock_code, start = '2017-12-01', end = today)
    csv_file = path.join(data_dir, stock_code + ".csv")
    if not path.exists(csv_file):
        return []
    df = pd.read_csv(csv_file)

    col = df.iloc[0:120,10]
    l = list(col.values)
    l.reverse()
    #print(len(l))
    return l

    """
    #ERROR
    #datatype is not correct, list of array(x)
    df_ma20 = df.iloc[:][['ma20']]
    l_ma20 = list(df_ma20.values)
    l_ma20.reverse()
    print(l_ma20)
    """


def check_turning(ma20):
    #print(ma20)
    flag_uptrend_last = True
    uptrend_days_last = 0

    flag_uptrend = True
    uptrend_days = 0

    last = -1

    for p in ma20:
        if last == -1:
            last = p
            continue

        flag_uptrend = p > last

        uptrend_days = uptrend_days + 1

        if flag_uptrend_last != flag_uptrend:
            flag_uptrend_last = flag_uptrend
            uptrend_days_last = uptrend_days
            uptrend_days = 0
        last = p

    if flag_uptrend:
        return uptrend_days

    return -1


def check_dense(ma20):
    change_percent = max(ma20)/min(ma20) - 1
    if change_percent < 0.1:
        return True
    return False


def loop_process():

    list_dense = []
    list_uptrend_40 = []
    list_uptrend_20 = []
    list_uptrend_5  = []
    list_uptrend_2_alone = []
    list_uptrend_1_alone = []
    for stock_code in list_stocks:
        ma20 = get_ma20(stock_code)
        if len(ma20) < 20:
            continue

        if check_dense(ma20) and len(ma20) > 30:
            print("%s筹码集中" % stock_code)
            list_dense.append(stock_code)
            continue

        turning_days = check_turning(ma20)
        if turning_days > 0:
             print("%s拐点在%d天前" % (stock_code, turning_days))

        if turning_days > 20 and turning_days < 40:
            list_uptrend_40.append(stock_code)

        if turning_days > 5:
            list_uptrend_20.append(stock_code)

        if turning_days > 0 and turning_days <= 5:
            list_uptrend_5.append(stock_code)

        if turning_days > 1 and turning_days <= 2:
            list_uptrend_2_alone.append(stock_code)

        if turning_days > 0 and turning_days <= 1:
            list_uptrend_1_alone.append(stock_code)

        #return

    print("****")
    print(" ".join(list_uptrend_5))
    print("****")
    print(" ".join(list_uptrend_2_alone))
    print("****")
    print(" ".join(list_uptrend_1_alone))
    print("****")


def up_limit_recents(days):



    pass



if __name__ == '__main__':

    #print(get_ma20("002709"))
    loop_process()



#end
