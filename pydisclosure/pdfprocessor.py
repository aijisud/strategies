# -*- coding: utf-8 -*-

from urllib.request import urlopen, urlretrieve
import requests

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from os import path

import csv
import time
from multiprocessing import Process
import logging

import pathhelper as ph

logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)

"""
logging.basicConfig()
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(filename)s][line:%(lineno)d] [%(levelname)-8s]: %(message)s')
ch.setFormatter(formatter)
logging.getLogger('').addHandler(ch)
"""

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
        urlretrieve(url, pdf_file)
        logging.error(url)
        logging.error(e)
        return

    #read ok, write to text
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)


def child_process(list_slice, start, txt_dir, pdf_dir):
    i = 0
    for row in list_slice:
        code, title, url = row
        file_name = str(i+start)
        txt_file = path.join(txt_dir, file_name + ".txt")
        pdf_file = path.join(pdf_dir, file_name + ".pdf")
        __save_to_txt(url, txt_file, pdf_file)
        i = i + 1

def process_csv_multiprocessing(csv_file, txt_dir, pdf_dir):
    if csv_file == "":
        csv_file = ph.get_csv_file_path()
    if txt_dir == "":
        txt_dir = ph.get_txt_directory()
    if pdf_dir == "":
        pdf_dir = ph.get_pdf_directory()

    with open(csv_file, encoding="utf-8") as f:

        file_rows = csv.reader(f)
        list_rows = list(file_rows)
        count = len(list_rows)
        print(count)

        if count <= 256:
            #single process
            child_process(list_rows, 0, txt_dir, pdf_dir)
            return

        #mutilprocessing
        processes = []
        start = 0
        stop = count
        step = round(count/15)
        last = 0

        for i in range(16):
            last = i
            stop = start + step
            if (stop > count):
                stop = count

            p_name = "process_no" + str(last)
            print(p_name)
            p = Process(name = p_name, target = child_process, \
                        args = (list_rows[start:stop], start, txt_dir, pdf_dir) )

            p.start()
            processes.append(p)

            start = stop

        for p in processes:
            p.join()

        print("all done...")

        #end of mutilprocessing

    #end of with (open) as f

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
        count = len(list_rows)
        print(count)

        i = 0
        for row in list_rows:
            code, title, url = row
            file_name = str(i)
            txt_file = path.join(txt_dir, file_name + ".txt")
            pdf_file = path.join(pdf_dir, file_name + ".pdf")
            __save_to_txt(url, txt_file, pdf_file)
            i = i + 1


if __name__ == "__main__":
    time_begin = time.strftime("%Y-%m-%d %H:%M:%S")
    print("time_begin:", time_begin)
    print("******************************")

    #process_csv("", "", "")
    process_csv("", "", "")


    time_end = time.strftime("%Y-%m-%d %H:%M:%S")
    print("******************************")
    print("time_end  :", time_end)


#end
