# -*- coding: utf-8 -*-

from urllib.request import urlopen
import requests

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from os import path

import csv
import time

import path_helpers as ph

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
    pdf_text = read_pdf(pdf_file)
    pdf_file.close()
    return pdf_text

def read_local_pdf(local_path):
    """
    use less
    """
    prefix = "file:/"
    pdf_file = urlopen(prefix + local_path)
    pdf_text = read_pdf(pdf_file)
    pdf_file.close()
    return pdf_text

def __example_read():
    """
    not in use
    """
    url = "http://www.cninfo.com.cn/finalpage/2017-08-03/1203758032.PDF"
    local_file = "E:/1203758032.PDF"
    text = read_online_pdf(url)
    print("example_read...")
    print(text)
    print("****************")


def __save_to_txt(url, text_file, pdf_file):
    try:
        text = read_online_pdf(url)
    except Exception as e:
        #fail to read, write to pdf
        urllib.urlretrieve(url, pdf_file)

    #read ok, write to text
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)


def process_csv(csv_file, txt_dir, pdf_dir):
    if csv_file == "":
        csv_file = ph.get_csv_file_path()
    if txt_dir == "":
        txt_dir = ph.get_txt_directory()
    if pdf_dir == "":
        pdf_dir = ph.get_pdf_directory()

    with open(csv_file, encoding="utf-8") as f:

        file_rows = csv.reader(f)
        list_rows = list(file_rows)
        print(len(list_rows))

        i = 1
        for row in list_rows:
            code, title, url = row
            txt_file = path.join(txt_dir, str(i) + ".txt")
            pdf_file = path.join(txt_dir, str(i) + ".pdf")
            __save_to_txt(url, txt_file, pdf_file)
            i = i + 1


if __name__ == "__main__":
    time_begin = time.strftime("%Y-%m-%d %H:%M:%S")
    print("time_begin:", time_begin)
    print("******************************")

    process_csv("", "", "")

    time_end = time.strftime("%Y-%m-%d %H:%M:%S")
    print("******************************")
    print("time_end  :", time_end)


#end
