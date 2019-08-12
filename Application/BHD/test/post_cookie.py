#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from urllib import parse


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '38',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'onepool.cc',
    'Origin': 'http://onepool.cc',
    'Referer': 'http://onepool.cc/eco-bhd/user/income_inquiry.html',
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 '
        'QQBrowser/10.4.3587.400'
    ),
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'loginName=mark3333520%40163.com; loginPwd=f3in2oWmp61%2FdHqnfanUzo6oqWKMjKnOl4h%2BmK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2FPv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2FpZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf; language=zh-CN; s4923fbb1=1ijvvh82q53c77jpckjtlbav61; Hm_lvt_2ed612fb19dda01a16e5619d19f0476f=1564293475,1564323606,1564493824,1564498812; Hm_lpvt_2ed612fb19dda01a16e5619d19f0476f=1564498812'
}
url = 'http://onepool.cc/eco_bhd/user/getincomeinquiry.html'
data = {'page': 1, 'start': '2019-07-30', 'stop': '2019-07-30'}

data = parse.urlencode(data).encode('utf-8')
req = request.Request(url=url, data=data, headers=headers)
resp = request.urlopen(req, timeout=3).read().decode('utf-8')
print(resp)
