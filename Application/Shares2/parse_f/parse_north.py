#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from traceback import format_exc

import gc
gc.set_threshold(50, 10, 10)
gc.enable()


def fetch():
    url = 'http://data.10jqka.com.cn/hsgt/timedia/type/north/'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    }
    try:
        req = requests.get(url, headers=headers, timeout=3)
        content = json.loads(req.content)
    except:
        pass
    return None

fetch()
