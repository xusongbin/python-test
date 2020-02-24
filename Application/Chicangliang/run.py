#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
import pyperclip
from lxml import etree
from traceback import format_exc


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'data.futures.hexun.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
}


def get(context='IC2003', date='2020-02-21'):
    url = 'http://data.futures.hexun.com/cccj.aspx?sContract={}&sDate={}&sRank=20'.format(context, date)
    try:
        resp = requests.get(url, headers=headers, timeout=3)
        # print(resp.text)
        selector = etree.HTML(resp.text)
        _amount_list = []
        _buy_list = []
        _sell_list = []
        for tr in selector.xpath('//div[@class="mainboxcontent"]/div[9]/table/tr[position()>=2]'):
            _seat = tr.xpath('td[1]/text()')[0].strip()
            _name = tr.xpath('td[2]/div/a/text()')[0].strip()
            _amount = tr.xpath('td[3]/text()')[0].strip()
            _amount_list.append([_seat, _name, _amount])
        for tr in selector.xpath('//div[@class="mainboxcontent"]/div[10]/table/tr[position()>=2]'):
            _seat = tr.xpath('td[1]/text()')[0].strip()
            _name = tr.xpath('td[2]/div/a/text()')[0].strip()
            _amount = tr.xpath('td[3]/text()')[0].strip()
            _buy_list.append([_seat, _name, _amount])
        for tr in selector.xpath('//div[@class="mainboxcontent"]/div[11]/table/tr[position()>=2]'):
            _seat = tr.xpath('td[1]/text()')[0].strip()
            _name = tr.xpath('td[2]/div/a/text()')[0].strip()
            _amount = tr.xpath('td[3]/text()')[0].strip()
            _sell_list.append([_seat, _name, _amount])
        return [_amount_list, _buy_list, _sell_list]
    except Exception as e:
        print('{}\n{}'.format(e, format_exc()))
    return None


def count(context='IC2003', date='2020-02-21'):
    _list = get(context, date)
    # for l in _list:
    #     print(l)
    _name_list = [x[1] for x in _list[1]]
    for ele in _list[2]:
        if ele[1] not in _name_list:
            _name_list.append(ele[1])
    _name_dict = {}
    for name in _name_list:
        _name_dict[name] = 0
    for ele in _list[1]:
        if ele[1] in _name_dict.keys():
            _name_dict[ele[1]] += int(ele[2])
    for ele in _list[2]:
        if ele[1] in _name_dict.keys():
            _name_dict[ele[1]] += int(ele[2])
    _name_dict = sorted(_name_dict.items(), key=lambda kv: [kv[1], kv[0]], reverse=True)
    # print(_name_dict)
    _name_list = [_name_dict[x][0] for x in range(20)]
    _value_list = [_name_dict[x][1] for x in range(20)]
    # _seat_list = [x+1 for x in range(20)]
    # pd.DataFrame({'名次': _seat_list, context: _name_list, date: _value_list}).to_excel('123.xlsx', index=None)
    return [_name_list, _value_list]


def put_clipboard(date='2020-02-21', top=10):
    try:
        IC2003 = count('IC2003', date)
        IF2003 = count('IF2003', date)
        _out = ''
        for idx in range(top):
            _out += '{}\t{}\t{}\t{}'.format(IC2003[0][idx], IC2003[1][idx], IF2003[0][idx], IF2003[1][idx])
            if idx < top-1:
                _out += '\n'
        pyperclip.copy(_out)
        return True
    except Exception as e:
        print('{}\n{}'.format(e, format_exc()))
    return False


def change_excel():
    ex_name = '持仓量.xlsx'
    ot_name = '持仓量1.xlsx'
    ex_df = pd.read_excel(ex_name)
    ex_list = ex_df.values.tolist()
    print(ex_list)
    resp_name = []
    resp_data = []
    for row in ex_list:
        resp_name.append(row[1])
    for name in resp_name:
        data = 0
        for row in ex_list:
            if row[1] == name:
                data += int(row[2])
            if row[4] == name:
                data += int(row[5])
        resp_data.append(data)
    resp = {}
    for idx, name in enumerate(resp_name):
        resp[name] = resp_data[idx]
    # print(resp)
    resp = sorted(resp.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(resp)
    for idx, row in enumerate(ex_list):
        ex_list[idx].append(idx+1)
        ex_list[idx].append(resp[idx][0])
        ex_list[idx].append(resp[idx][1])
    print(ex_list)
    dd = pd.DataFrame(ex_list)
    print(dd)
    dd.to_excel(ot_name, index=None)


if __name__ == '__main__':
    date = input('请输入日期：')
    result = put_clipboard(date)
    if result:
        print('已获取{}数据到剪切板'.format(date))
    else:
        print('获取数据异常，请检查网络及日期是否正确。（2020-02-21）')
