# -*- coding: UTF-8 -*-

from urllib.request import urlopen
import requests

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

import csv
import time
#from io import open

def read_pdf(pdf_file):
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    laparams = LAParams()
    device = TextConverter(resource_manager, return_string, laparams=laparams)

    process_pdf(resource_manager, device, pdf_file)
    device.close()

    content = return_string.getvalue()
    return_string.close()
    return content


def read_online_pdf(url):
    pdf_file = urlopen(url)
    #print(pdf_file)
    pdf_text = read_pdf(pdf_file)
    pdf_file.close()
    return pdf_text

def read_local_pdf(url):
    pdf_file = open(url)
    print(pdf_file)
    pdf_text = read_pdf(pdf_file)
    pdf_file.close()
    return pdf_text

def example_read():
    url = "http://www.cninfo.com.cn/finalpage/2017-08-03/1203758032.PDF"
    prefix = "file:/"
    local_file = "E:/1203758032.PDF"
    text = read_online_pdf(url)
    print(text)
    print("****************")

if __name__ == "__main__":
    i = 0
    error_count = 0
    error_list = []
    time_begin = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("20170825-111.csv", encoding="utf-8") as f:
        rows = csv.reader(f);
        list_rows = list(rows)
        print(len(list_rows))

        for pdf in list_rows:
            title, url = pdf
            #print(title)
            #print(url)
            try:
                text = read_online_pdf(url)
            except Exception as e:
                #print(e)
                error_list.append(pdf)
                error_count = error_count + 1
            i = i + 1

            print(i, error_count)

    time_end = time.strftime("%Y-%m-%d %H:%M:%S")

    print("******************************")
    print("******************************")
    print("******************************")

    print(error_list)
    print("time_begin:", time_begin)
    print("time_end  :", time_end)

#end
