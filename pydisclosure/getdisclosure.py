# -*- coding: UTF-8 -*-
import requests
from lxml import etree
from lxml import html
import json
import csv
import configparser
import time
from datetime import date, timedelta
import os


CONFIG  = "c.conf"

def get_target_file_path():
    c = configparser.ConfigParser()
    c.read(CONFIG)
    base_dir = c.get("path", "base_directory")

    today = date.today().strftime("%Y%m%d")
    tomorrow = (date.today() + timedelta(1)).strftime("%Y%m%d")

    parent_parent = os.path.dirname(os.path.dirname(os.path.abspath('.')))

    path = os.path.join(parent_parent, base_dir, today)
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(parent_parent, base_dir, today, today + ".csv")

    return file_path


def get_sse_disclosure():

    base_url = "http://www.sse.com.cn/disclosure/listedinfo/announcement/"
    base_url_post = "http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Origin': 'http://www.sse.com.cn',
        'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
        'Host': 'www.sse.com.cn',
    }

    s = requests.Session()
    r = s.post(base_url_post, headers = headers)

    #使用r.content转码为utf-8
    page = etree.HTML(r.content.decode('utf-8'))

    """
    dds = page.xpath(u'//dd[@class="just_this_only"]')
    for dd in dds:
        dd_html = etree.HTML(html.tostring(dd))
        title = dd_html.xpath(u'//a[@class="hidden-xs"]/@title')
        print(title)
        break

    hrefs = page.xpath(u'//a[@class="hidden-xs"]')
    #print(hrefs)
    for href in hrefs:
        print(href.get('title'))
        print(href.get('href'))
        return
    """

    em_hrefs = page.xpath(u'//em[@class="pdf-first"]/a')
    #print(em_hrefs)

    disclosures = []

    for em_href in em_hrefs:
        disclosure_code, disclosure_title = em_href.text.split("：\t")
        disclosure_pdf_url = em_href.get('href')
        #print( "%s %s" % (disclosure_title, disclosure_pdf_url))
        disclosures.append([disclosure_code, disclosure_title, disclosure_pdf_url])

    return (disclosures)

def get_szse_disclosure():

    pdf_base_url = "http://www.cninfo.com.cn/"
    base_url_post = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse_latest"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Origin': 'http://www.cninfo.com.cn',
        'Referer': 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse',
        'Host': 'www.cninfo.com.cn',
    }

    post_data = {
        #stock=&searchkey=&plate=&category=&trade=&
        #column=szse&
        #columnTitle=%E6%B7%B1%E5%B8%82%E5%85%AC%E5%91%8A&pageNum=5&pageSize=30&
        #tabName=latest&
        #sortName=&sortType=&limit=&
        #showTitle=&seDate=%E8%AF%B7%E9%80%89%E6%8B%A9%E6%97%A5%E6%9C%9F

        "column": "szse",

        "columnTitle": "深市公告",
        "pageNum": 99,
        "pageSize": 30,

        "tabName": "latest",
        "seDate": "请选择日期",
    }

    disclosures = []
    pageNum = 1

    s = requests.Session()
    while True:
        post_data["pageNum"] = pageNum
        pageNum = pageNum + 1

        r = s.post(base_url_post, headers = headers, data = post_data)
        #使用r.content转码为utf-8
        r_json = r.content.decode('utf-8')

        r_dict = json.loads(r_json)
        #先处理

        for all_disclosures_in_one_stock in r_dict["classifiedAnnouncements"]:
            for one_disclosure in all_disclosures_in_one_stock:
                disclosure_code = one_disclosure["secCode"]
                disclosure_title = "[%s]%s" % (one_disclosure["secName"], one_disclosure["announcementTitle"])
                disclosure_pdf_url = pdf_base_url + one_disclosure["adjunctUrl"]
                disclosures.append([disclosure_code, disclosure_title, disclosure_pdf_url])

        if r_dict["hasMore"]:
            continue
        else:
            break

    return (disclosures)

def get_all_pdfs():
    disclosures = get_sse_disclosure()
    szse = get_szse_disclosure()
    disclosures.extend(szse)
    return disclosures

def save_to_csv(data_list):
    with open( get_target_file_path(), "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for data in data_list:
            csv_writer.writerow(data)

def get_all_and_save():
    """
    get_all_pdfs()
    save_to_csv()
    i.e.
        pdfs = get_all_pdfs()
        save_to_csv(pdfs)
    """
    print("begin to get disclosures...")
    disclosures = get_sse_disclosure()
    print("got disclosures of sse...")
    szse = get_szse_disclosure()
    print("got disclosures of szse...")
    disclosures.extend(szse)
    with open( get_target_file_path(), "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for d in disclosures:
            csv_writer.writerow(d)
    print("saved to csv...")
    return disclosures


if __name__ == "__main__":
    get_all_and_save()



#end
