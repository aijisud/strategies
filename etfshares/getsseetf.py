# -*- coding: utf-8 -*-

import requests
import os
import json
import time
import csv
import codecs

from datetime import datetime, date, timedelta

cwd = os.getcwd()

BASE_URL = "http://query.sse.com.cn/commonQuery.do"
FULL_URL = "http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback56197&isPagination=true&sqlId=COMMON_SSE_ZQPZ_ETFZL_XXPL_ETFGM_SEARCH_L&pageHelp.pageSize=10000&STAT_DATE=2018-01-05&_=1520939130943"

headers = {
    'Host': 'query.sse.com.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://www.sse.com.cn/market/funddata/volumn/etfvolumn/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'yfx_c_g_u_id_10000042=_ck17071501170614759365750711339; VISITED_FUND_CODE=%5B%22512330%22%5D; yfx_mr_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000042=; VISITED_COMPANY_CODE=%5B%22512330%22%2C%22600870%22%2C%22603988%22%2C%22600012%22%5D; VISITED_STOCK_CODE=%5B%22600870%22%2C%22603988%22%2C%22600012%22%5D; seecookie=%u4E0A%u8BC150%2C%5B512330%5D%3A500%u4FE1%u606F%2C%5B600870%5D%3A%u53A6%u534E%u7535%u5B50%2C%u6CAA%u6DF1300%2C%5B603988%5D%3A%u4E2D%u7535%u7535%u673A%2C%5B600012%5D%3A%u7696%u901A%u9AD8%u901F; yfx_mr_f_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; VISITED_MENU=%5B%228758%22%2C%228629%22%2C%228630%22%2C%228631%22%2C%2210574%22%2C%228618%22%2C%228619%22%2C%228620%22%2C%228349%22%2C%228451%22%2C%228491%22%5D; yfx_f_l_v_t_10000042=f_t_1500052626445__r_t_1520939093716__v_t_1520957893951__r_c_20',
}

params = {
    'jsonCallBack': 'jsonpCallback22993',
    'isPagination': 'true',
    'sqlId': 'COMMON_SSE_ZQPZ_ETFZL_XXPL_ETFGM_SEARCH_L',
    'pageHelp.pageSize': '10000',
    'STAT_DATE': '2018-03-06',
    '_': '1520957937405',
}


s = requests.Session()


def get_sse_etf(stat_date):
    params["STAT_DATE"] = stat_date
    r = s.get(BASE_URL, headers = headers, params = params)
    j = r.text.lstrip("jsonpCallback22993(").rstrip(")")
    d = json.loads(j)
    csv_content = d["pageHelp"]["data"]
    return csv_content


def save_to_csv(csv_content, file_name):

    #下一行存在直接用excel打开乱码，用编辑模式记事本打开正确的情况
    #with open(file_name, "w", encoding="utf-8", newline="") as csv_file:

    with codecs.open(file_name, "w", encoding="utf_8_sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        for d_row in csv_content:
            #ETF_TYPE	NUM	SEC_NAME	STAT_DATE	SEC_CODE	TOT_VOL
            row = [d_row["ETF_TYPE"], d_row["NUM"], d_row["SEC_NAME"], d_row["STAT_DATE"], d_row["SEC_CODE"], d_row["TOT_VOL"].strip()]
            csv_writer.writerow(row)


def get_full_year(year):

    first = str(year) + "-01-01"
    csv_content = []

    file_name = os.path.join(cwd, "data", str(year) + ".csv")
    print(file_name)

    i = 3
    while i < 5:
        stat_date = (datetime.strptime(first, "%Y-%m-%d") + timedelta(i)).strftime("%Y-%m-%d")
        if stat_date[0:4] == str(int(year) + 1):
            break
        each_day = get_sse_etf(stat_date)
        time.sleep(3)
        csv_content.extend(each_day)
        i = i + 1
        print(i)

    save_to_csv(csv_content, file_name)
    print("done")


if __name__ == "__main__":

    """
    csv_content = get_sse_etf("2012-01-01")
    if csv_content:
        print(csv_content)
    else:
        print("empty")

    csv_content = get_sse_etf("2012-01-04")
    if csv_content:
        print(csv_content)
    """

    get_full_year(2012)



#end
