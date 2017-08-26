# -*- coding: utf-8 -*-
import configparser
import codecs
import time
from datetime import date, timedelta
from os import path, makedirs


CONFIG  = "c.conf"

c = configparser.ConfigParser()
c.readfp(codecs.open(CONFIG, "r", "utf-8-sig"))

base_dir = c.get("path", "base_directory")

today = date.today().strftime("%Y%m%d")
tomorrow = (date.today() + timedelta(1)).strftime("%Y%m%d")

parent_parent = path.dirname(path.dirname(path.abspath('.')))

def __get_current_day():
    day = today
    if int(time.strftime("%H")) < 12:
        day = today
    else:
        day = tomorrow
    return day

def get_csv_file_path():

    str_date = __get_current_day()

    base_path = path.join(parent_parent, base_dir, str_date)

    if not path.exists(base_path):
        makedirs(base_path)

    file_path = path.join(base_path, str_date + ".csv")
    return file_path


def get_pdf_directory():
    str_date = __get_current_day()

    directory = path.join(parent_parent, base_dir, str_date, "pdf")

    if not path.exists(directory):
        makedirs(directory)

    return directory


def get_txt_directory():
    str_date = __get_current_day()

    directory = path.join(parent_parent, base_dir, str_date, "txt")

    if not path.exists(directory):
        makedirs(directory)

    return directory


if __name__ == "__main__":
    print(get_csv_file_path())
    print(get_pdf_directory())
    print(get_txt_directory())

#end
