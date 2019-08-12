#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from urllib import parse

url = 'http://www.qbtc.ink/json/depthTable.do?tradeMarket=CNYT&symbol=BURST'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 '
        'QQBrowser/10.4.3587.400'
    )
}
req = request.Request(url=url, headers=headers)
resp = request.urlopen(req, timeout=3)
print(resp.read().decode())
