# -*- coding: utf-8 -*-

"""
小停牌战法
直接打印筛选结果，并保存csv
"""


import requests
import re
import os
#from lxml import etree, html
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import xlrd
import datetime
from datetime import datetime, date, timedelta
import types
import csv

CSV_DIR = "data"

BASE_EXCEL_URL = "http://www.csrc.gov.cn/pub/zjhpublic/G00306207/201210/"
URL_EXCEL = "http://www.csrc.gov.cn/pub/zjhpublic/G00306207/201210/t20121015_215829.htm"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
}

FIRST_DAY = datetime.strptime("19000101", "%Y%m%d")




"""
URL0 = "http://www.csrc.gov.cn/pub/zjhpublic/832/index_7401.htm"
URL1 = "http://www.csrc.gov.cn/pub/zjhpublic/832/index_7401_1.htm"
URL2 = "http://www.csrc.gov.cn/pub/zjhpublic/832/index_7401_2.htm"
"""

def __get_excel_url():
    s = requests.Session()
    r = s.get(URL_EXCEL, headers = headers)
    bs = BeautifulSoup(r.content.decode("utf-8"), 'html.parser')
    a = bs.find('a', attrs = { "href" : re.compile(".*xls") })
    return BASE_EXCEL_URL + a["href"]

def download_excel():
    """
    解析结果，下载excel保存到对应目录
    """
    s = requests.Session()
    r = s.get(URL_EXCEL, headers = headers)
    bs = BeautifulSoup(r.content.decode("utf-8"), 'html.parser')
    a = bs.find('a', attrs = { "href" : re.compile(".*xls") })
    excel_url = BASE_EXCEL_URL + a["href"]

    file_name = excel_url.split("/")[-1]
    excel_file = os.path.join(CSV_DIR, file_name)
    urlretrieve(excel_url, excel_file)
    return excel_file


def __parse_excel_example():
    data = xlrd.open_workbook(excelFile)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    for i in xrange(0,nrows):
        rowValues= table.row_values(i) #某一行数据
        for item in rowValues:
            print(item)


def parse_excel(excel_file):
    """
    从excel文件中读取数据
    """
    data = xlrd.open_workbook(excel_file)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    l = []
    for i in range(2, nrows - 2):
        l.append(table.row_values(i))
    return l


"""
bug in excel
1900/1/1  -- 1
1900/2/28 -- 59
1900/2/29 -- 60 -- BUG HERE
1900/3/1  -- 61
"""

"""
timedelta
1900/1/1 + 1 = 1900/1/2
"""


"""
['序号', '上市公司简称', '股票代码', '申请人', '申请项目',
'审核类型', '接收日期', '补正日期', '受理日期', '反馈日期',
'反馈回复日期', '并购重组委会议日期', '审结日期', '备注', '独立财务顾问',
'独立财务顾问主办人', '财务顾问', '财务顾问主办人', '律师事务所', '签字律师',
'会计师事务所', '签字会计师', '资产评估机构/估值机构', '签字评估师/估值人员']
"""

def parse_date(data):
    """
    解析单元格中日期
    2016-12-2 2017-1-18
    或者读出来数字42860
    """
    reply_date = FIRST_DAY
    if isinstance(data, str):
        #多个日期
        str_2 = data.replace("  ", " ").replace("\n", " ")
        if len(str_2) > 8:
            #正确分析出是两个日期
            temp, date_str = str_2.split(" ")
            reply_date = datetime.strptime(date_str, "%Y-%m-%d")

    if isinstance(data, float):
        #一个日期被转为了数字
        reply_date = FIRST_DAY + timedelta(int(data) - 2)

    return reply_date


def format_print(r):
    """
    格式化输出
    """
    empty_date = "0000-00-00"
    return [int(r[0]), r[1], str(r[2]).replace(".0", ""), r[3], r[4], r[5], \
        parse_date(r[6]).strftime("%Y-%m-%d"), \
        empty_date if r[7] == "" else parse_date(r[7]).strftime("%Y-%m-%d"), \
        empty_date if r[8] == "" else parse_date(r[8]).strftime("%Y-%m-%d"), \
        empty_date if r[9] == "" else parse_date(r[9]).strftime("%Y-%m-%d"), \
        parse_date(r[10]).strftime("%Y-%m-%d"), \
        ]


def extract_data(list_data):
    """
    解析日期，筛选数据，格式化输出
    """
    r = list_data[0]
    result_list = []
    result_list.append(
            [r[0], r[1].replace("\n",""), r[2].replace("\n",""), r[3], \
            r[4].replace("\n",""), r[5], r[6], r[7], r[8], r[9], r[10].replace("\n","")]
            )
    for r in list_data:
        #print(r[5])
        #审核类型
        #并购重组委会议日期
        #备注
        #反馈回复日期, 近一周内
        if r[5] == "正常审核" and r[11] == "" and r[13] == "" and r[10] != "":
            reply_date = parse_date(r[10])
            if reply_date > FIRST_DAY and reply_date + timedelta(20) > datetime.now():
                result_list.append(format_print(r))

    return result_list


def do():

    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "start to download..."))
    excel_file = download_excel()

    excel_date = excel_file.split("W0")[1][0:8]

    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "strat to exctract data..."))

    data_list = extract_data(parse_excel(excel_file))
    print("************************************************************************************************")

    csv_file = os.path.join(CSV_DIR, excel_date+".csv")
    with open( csv_file, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for data in data_list:
            csv_writer.writerow(data)
            print(data)

    print("************************************************************************************************")

    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "saved to csv and latest.csv"))


if __name__ == "__main__":

    do()



#end
