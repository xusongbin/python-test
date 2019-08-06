#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time
import json
import gzip
from urllib import request
from urllib import parse

tms = int(time()*1000)
url = 'https://www.wacai.com/setting/account_list.action?timesamp={}'.format(tms)

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '58',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': (
        'JSESSIONID=2A3A9A2AAC5BDFEE5E120CC149EC8EC4; '
        'sajssdk_2015_cross_new_user=1; '
        'sensorsdata2015jssdkcross=%7B%22'
        'distinct_id%22%3A%22'
        '16c461828eb4c2-024faca9e80597-48774f16-1049088-16c461828ec28d%22%2C%22%24'
        'device_id%22%3A%2216c461828eb4c2-024faca9e80597-48774f16-1049088-16c461828ec28d%22%2C%22'
        'props%22%3A%7B%22%24latest_'
        'referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24'
        'latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24'
        'latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_'
        '%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; '
        'wctk=WCeO2k48oZiiwLIPYLKsjchOPolRnG38-yWkg; '
        'wctk.sig=vt9wZb8DOvb2r05zFJBKMglKy8o; '
        'access_token=WCeO2k48oZiiwLIPYLKsjchOPolRnG38-yWkg; '
        'access_token.sig=fqcO8kx1zuN3VWnD1ldC2zsh6NI;'
    ),
    'Host': 'www.wacai.com',
    'Origin': 'https://www.wacai.com',
    'Referer': 'https://www.wacai.com/user/user.action',
    'User-Agent': (
        'Mozilla/5.0 '
        '(Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 '
        '(KHTML, like Gecko) '
        'Chrome/70.0.3538.25 '
        'Safari/537.36 Core/1.70.3722.400 '
        'QQBrowser/10.5.3738.400'
    ),
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
    'type': 'all',
    'reqBalance': 'true',
    'pageInfo.pageIndex': '1',
    'hidden': 'false'
}

data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, data, headers)
resp = request.urlopen(req)

if resp.info().get('Content-Encoding') == 'gzip':
    resp = gzip.decompress(resp.read()).decode('utf-8')
else:
    resp = resp.read().encode('utf-8')

resp_dict = json.loads(resp)
value = 0
for account in resp_dict['accountTypeSum']:
    if 'accTypeName' not in account.keys():
        continue
    if account['accTypeName'] == '投资账户':
        for accs in account['accs']:
            if accs['name'] == '矿工':
                value = accs['balance']
print(value)

