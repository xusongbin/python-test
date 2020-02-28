#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyperclip
import numpy
from bs4 import BeautifulSoup

from my_driver import *


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
        soup = BeautifulSoup(resp.text, 'html.parser')
        _list = [x.string.strip() for x in soup.find_all('td') if x.string]
        _nlist = numpy.array(_list).reshape((3, 21, 4))
        # print(_nlist)
        print('{}\t{}'.format(date, context))
        for (buy, sell) in zip(list(_nlist[1, :, :]), list(_nlist[2, :, :])):
            print('{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}'.format(buy[0], buy[1], buy[2], sell[0], sell[1], sell[2]))
        return _nlist
    except Exception as e:
        print('{}\n{}'.format(e, format_exc()))
    return None


def count(context='IC2003', date='2020-02-21'):
    _nlist = get(context, date)
    _buy_name = list(_nlist[1, 1:, 1])
    _buy_value = list(_nlist[1, 1:, 2])
    _buy_dict = dict(zip(_buy_name, _buy_value))
    _sell_name = list(_nlist[2, 1:, 1])
    _sell_value = list(_nlist[2, 1:, 2])
    _sell_dict = dict(zip(_sell_name, _sell_value))
    _total_name = list(set(_buy_name + _sell_name))
    _total_value = dict(zip(_total_name, [0 for _ in range(len(_total_name))]))
    for name in _total_value.keys():
        if name in _buy_dict.keys():
            _total_value[name] += int(_buy_dict[name])
        if name in _sell_dict.keys():
            _total_value[name] += int(_sell_dict[name])
    # print(_total_value)
    _total_value_s = {k: _total_value[k] for k in sorted(_total_value, key=_total_value.__getitem__, reverse=True)}
    # print(_total_value_s)
    return [list(_total_value_s.keys()), list(_total_value_s.values())]


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


def main():
    yesterday = strftime("%Y-%m-%d", localtime())
    pyperclip.copy(yesterday)
    date = input('请输入日期（默认昨天的日期，可黏贴）：')
    date = date.strip()
    if not date:
        date = yesterday
    result = put_clipboard(date)
    if result:
        print('已获取{}数据到剪切板'.format(date))
    else:
        print('获取数据异常，请检查网络及日期是否正确。（2020-02-21）')
    os.system('pause')


if __name__ == '__main__':
    main()
    # get()
    # count()
