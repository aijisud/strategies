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
import time
import shutil
import wget

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

def __download_excel():
    """
    解析结果，通过urlretrieve下载excel保存到对应目录
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


def download_excel(target_dir):
    """
    解析结果，下载excel保存到对应目录
    """
    s = requests.Session()
    r = s.get(URL_EXCEL, headers = headers)
    bs = BeautifulSoup(r.content.decode("utf-8"), 'html.parser')
    a = bs.find('a', attrs = { "href" : re.compile(".*xls") })
    excel_url = BASE_EXCEL_URL + a["href"]

    download_file_name = excel_url.split("/")[-1]

    if os.path.exists(download_file_name):
        os.remove(download_file_name)
    if os.path.exists(os.path.join(target_dir, download_file_name)):
        os.remove(os.path.join(target_dir, download_file_name))

    file_name = wget.download(excel_url)
    shutil.move(file_name, target_dir)
    excel_file = os.path.join(target_dir, file_name)
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
def parse_date_one(data):
    """
    解析单元格中日期
    2017-1-18
    或者读出来数字42860
    """
    reply_date = FIRST_DAY
    if isinstance(data, str):
        return data.replace("  ", " ").replace("\n", " ").strip()

    if isinstance(data, float):
        #一个日期被转为了数字
        return FIRST_DAY + timedelta(int(data) - 2)

    return reply_date


def parse_date_two(data):
    """
    解析单元格中日期
    2016-12-2 2017-1-18
    或者读出来数字42860
    """
    date_0 = FIRST_DAY
    date_1 = FIRST_DAY

    if isinstance(data, str):
        #多个日期
        str_two = data.replace("  ", " ").replace("\n", " ")
        if len(str_two) > 8:
            #正确分析出是两个日期
            date_0_str, date_1_str = str_two.split(" ")
            date_0 = datetime.strptime(date_0_str, "%Y-%m-%d")
            date_1 = datetime.strptime(date_1_str, "%Y-%m-%d")

    if isinstance(data, float):
        #一个日期被转为了数字
        date_0 = FIRST_DAY + timedelta(int(data) - 2)

    return [date_0, date_1]


"""
['序号', '上市公司简称', '股票代码', '申请人', '申请项目',
'审核类型', '接收日期', '补正日期', '受理日期', '反馈日期',
'反馈回复日期', '并购重组委会议日期', '审结日期', '备注', '独立财务顾问',
'独立财务顾问主办人', '财务顾问', '财务顾问主办人', '律师事务所', '签字律师',
'会计师事务所', '签字会计师', '资产评估机构/估值机构', '签字评估师/估值人员']

[61.0, '上海电力', 600021.0, '上海电力', '发行股份购买资产',
'正常审核', 42913.0, '', 42916.0, 42947.0, 42985.0,
'', '', ' ', '国泰君安证券股份有限公司', '辛爽   寻国良',
'无', '无', '北京 市中咨律师事务所', '贾向明叶蔓青', '信永中和会计师事务所（特殊普通合伙）',
'郑卫军    廖志勇', '上海东洲资产评估有限公司', '吴元晨武钢']

"""

def data_cleaning(r):
    """
    数据清洗
    list --> list

    """

    feedback_date_first, feedback_date_second = parse_date_two(r[9])
    reply_date_first, reply_date_second = parse_date_two(r[10])

    """
    '序号', '上市公司简称', '股票代码',
    '申请项目',
    '接收日期',
    '补正日期', '受理日期',

    '首次反馈日期', '首次反馈回复',
    '二次反馈日期', '二次反馈回复',

    # -4 反馈回复日期, 近一周内
    # -3 备注
    # -2 并购重组委会议日期
    # -1 审核类型
    """

    row = [
            int(r[0]), \
            r[1].replace("\n", "").strip(), \
            str(int(r[2])) if isinstance(r[2], float) else r[2].strip(), \
            r[4].replace("\n", "").strip(), \
            parse_date_one(r[6]), \
            FIRST_DAY if str(r[7]).strip() == "" else parse_date_one(r[7]), \
            FIRST_DAY if str(r[8]).strip() == "" else parse_date_one(r[8]), \
            feedback_date_first, \
            reply_date_first, \
            feedback_date_second, \
            reply_date_second, \

            reply_date_second if reply_date_second > reply_date_first else reply_date_first, \
            r[13].replace("\n", "").strip(), \
            str(r[11]).strip(), \
            r[5].replace("\n", "").replace(" ", ""), \
          ]

    return row


def parse_excel(excel_file):
    """
    从excel文件中读取数据
    """
    data = xlrd.open_workbook(excel_file)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    l = []
    for i in range(3, nrows - 2):
        #start with 3, exclude the headers
        row = table.row_values(i)
        if isinstance(row[0], float) or isinstance(row[0], int):
            l.append(data_cleaning(row))
    return l


"""
'序号', '上市公司简称', '股票代码',
'申请项目',
'接收日期',
'补正日期', '受理日期',

'首次反馈日期', '首次反馈回复',
'二次反馈日期', '二次反馈回复',

# -4 反馈回复日期, 近一周内
# -3 备注
# -2 并购重组委会议日期
# -1 审核类型
"""

"""
def format_date(d):
    return "-" if d.year == 1900 else d.strftime("%Y-%m-%d")
"""

def extract_data(list_data):
    """
    解析日期，筛选数据，格式化输出
    """
    csv_header =   ['序号', '上市公司简称', '股票代码', '申请项目', \
                    '接收日期', '补正日期', '受理日期', \
                    '首次反馈日期', '首次反馈回复', \
                    '二次反馈日期', '二次反馈回复']

    result_list = []
    result_list.append(csv_header)

    format_date = lambda d : "-" if d.year == 1900 else d.strftime("%Y-%m-%d")

    for r in list_data:
        #print(r[5])
        # -1 审核类型
        # -2 并购重组委会议日期
        # -3 备注
        # -4 反馈回复日期, 近一周内
        #print(r)
        if  r[-1] == "正常审核" \
            and r[-2] == "" \
            and r[-3] == "" \
            and r[-4] + timedelta(20) > datetime.now() :

            result_list.append([r[0], r[1], r[2], r[3], \
                                format_date(r[4]), format_date(r[5]), format_date(r[6]), \
                                format_date(r[7]), format_date(r[8]), format_date(r[9]), \
                                format_date(r[10]),])
            """
            result_list.append([r[0], r[1], r[2], r[3], \
                                "-" if r[4].year == 1900 else r[4].strftime("%Y-%m-%d"), \
                                "-" if r[5].year == 1900 else r[5].strftime("%Y-%m-%d"), \
                                "-" if r[6].year == 1900 else r[6].strftime("%Y-%m-%d"), \
                                "-" if r[7].year == 1900 else r[7].strftime("%Y-%m-%d"), \
                                "-" if r[8].year == 1900 else r[8].strftime("%Y-%m-%d"), \
                                "-" if r[9].year == 1900 else r[9].strftime("%Y-%m-%d"), \
                                "-" if r[10].year == 1900 else r[10].strftime("%Y-%m-%d"), \
                                ])
            """

    return result_list


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


def do():
    cwd = os.getcwd()
    print("cwd is", cwd)
    target_dir = os.path.join(cwd, CSV_DIR)

    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "start to download..."))
    excel_file = download_excel(target_dir)
    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "downloaded..."))

    excel_date = excel_file.split("W0")[1][0:8]
    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "strat to exctract data..."))

    cleaned_data = parse_excel(excel_file)

    data_list = extract_data(cleaned_data)

    print("************************************************************************************************")

    csv_file = os.path.join(target_dir, excel_date+".csv")
    with open( csv_file, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for data in data_list:
            csv_writer.writerow(data)
            print(data)

    print("************************************************************************************************")

    print("[%s]%s" % (time.strftime("%Y%m%d %H%M%S"), "saved to csv"))


if __name__ == "__main__":

    do()



#end
