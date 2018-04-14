# -*- coding: utf-8 -*-

import csv
import copy

#reverse 反转
#recover 反弹

grtr = []
less = []

#十字星
doji = []

monitor_stocks = []

csv_file = "monitoring.csv"

def get_greater_less_list():
    with open(csv_file, encoding="utf-8") as f:
        rows = list(csv.reader(f))
        for row in rows:
            if row[2] == "<":
                less.append(row)
            elif row[2] == ">":
                grtr.append(row)
            elif row[2] == "+":
                doji.append(row)
        monitor_stocks.extend(rows)


def get_hq():
    pass


if __name__ == '__main__':
    get_greater_less_list()
    print(monitor_stocks)
    print(grtr)
    print(less)





#end
