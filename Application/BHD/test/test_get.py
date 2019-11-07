#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from urllib import parse


headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
    )
}
url = 'https://openapi.bitmart.io/v2/ticker?symbol={}_BHD'.format('LHD')
req = request.Request(url=url, headers=headers)
resp = request.urlopen(req, timeout=10)

context = resp.read().decode('utf-8')
print(context)
