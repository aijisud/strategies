# -*- coding: utf-8 -*-
import requests


def monitor():
    print("monitor")

def get_szse_midclose_disclosures():

    base_url = "http://disclosure.szse.cn//disclosure/fulltext/plate/szlatest_24h.js?ver=201710131259"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    }

    s = requests.Session()
    r = s.get(base_url, headers = headers)

    raw = r.content.decode('gbk')
    l = eval(raw[17:-2])
    print(l)


if __name__ == "__main__":
    get_szse_midclose_disclosures()
    exit(0)
