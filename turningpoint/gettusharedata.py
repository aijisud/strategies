# -*- coding: utf-8 -*-

import time
import tushare as ts
import os
from os import path


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


def save_hist_data(stock_code):
    df = ts.get_hist_data(stock_code)
    csv_file = path.join(data_dir, stock_code + ".csv")
    if os.path.exists(csv_file):
        print("%s exists" % stock_code)
        return
    if df is None:
        print("%s is none" % stock_code)
        return
    df.to_csv(csv_file)
    print("%s saved" % stock_code)

def loop_process():
    for stock_code in list_stocks:
        save_hist_data(stock_code)


if __name__ == '__main__':
    #save_hist_data('002709')
    loop_process()




#end
