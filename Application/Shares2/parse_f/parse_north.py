#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


def fetch():
    url = 'http://data.10jqka.com.cn/hsgt/basedata/type/north/'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    }
    req = requests.get(url, headers=headers)
    print(req.content)


fetch()
