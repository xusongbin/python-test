#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
from urllib import request
from urllib import parse

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': (
        'loginName=mark3333520%40163.com; '
        'loginPwd=f3in2oWmp61%2F'
        'dHqnfanUzo6oqWKMjKnOl4h%2B'
        'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
        'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
        'pZySgXu3mJHPrKN%2'
        'FqoJkic6rz47LvZ98o2Wf;'
    ),
    'Host': 'onepool.cc',
    'Referer': 'http://onepool.cc/eco-bhd/user/income_inquiry.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 '
        'Safari/537.36 Core/1.70.3704.400 '
        'QQBrowser/10.4.3587.400'
    )
}

url = 'http://onepool.cc/eco-bhd/user/asset.html'

req = request.Request(url=url, headers=headers)
resp = request.urlopen(req, timeout=3)
info = resp.info()

if ('Content-Encoding' in info and info['Content-Encoding'] == 'gzip') or ('content-encoding' in info and info['content-encoding'] == 'gzip'):
    resp = gzip.decompress(resp.read()).decode('utf-8')
else:
    resp = resp.read().decode('utf-8')
print(resp)
