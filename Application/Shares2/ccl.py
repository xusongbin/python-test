#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from bs4 import BeautifulSoup

from myDriver import *


class Ccl(object):
    __headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'data.futures.hexun.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
    }

    def __init__(self):
        pass

    def get_data(self, context='IC2003', date='2020-02-21'):
        url = 'http://data.futures.hexun.com/cccj.aspx?sContract={}&sDate={}&sRank=20'.format(context, date)
        try:
            resp = requests.get(url, headers=self.__headers, timeout=3)
            soup = BeautifulSoup(resp.text, 'html.parser')
            _list = [x.string.strip() for x in soup.find_all('td') if x.string]
            if len(_list) != 252:
                return None
            _nlist = numpy.array(_list).reshape((3, 21, 4))
            # print('{}\t{}'.format(date, context))
            # for (buy, sell) in zip(list(_nlist[1, :, :]), list(_nlist[2, :, :])):
            #     print('{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}'.format(buy[0], buy[1], buy[2], sell[0], sell[1], sell[2]))
            return _nlist
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return None

    def count(self, _nlist):
        try:
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
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None

    def get(self, _date=None, show=False, top=10, year='2006'):
        if not _date:
            _date = strftime("%Y-%m-%d", localtime())
        # _date = '2020-02-27'
        _nlist1 = self.get_data('IC{}'.format(year), _date)
        _nlist2 = self.get_data('IF{}'.format(year), _date)
        if show:
            print('{}\t{}'.format(_date, 'IC{}'.format(year)))
            for i in range(1, 11):
                print('{:<4}\t{:<10}\t{:<4}\t{:<10}'.format(
                    _nlist1[1][i][1], _nlist1[1][i][2], _nlist1[2][i][1], _nlist1[2][i][2]
                ))
            print('{}\t{}'.format(_date, 'IF{}'.format(year)))
            for i in range(1, 11):
                print('{:<4}\t{:<10}\t{:<4}\t{:<10}'.format(
                    _nlist2[1][i][1], _nlist2[1][i][2], _nlist2[2][i][1], _nlist2[2][i][2]
                ))
        try:
            # _old = '{}\t{}\t{}\t{}'.format(_nlist1[1][1][1], _nlist1[1][1][2], _nlist2[1][1][1], _nlist2[1][1][2])
            _old = '{}\t{}'.format(_nlist1[1][1][2], _nlist2[1][1][2])
            _clist1 = self.count(_nlist1)
            _clist2 = self.count(_nlist2)
            _count = ''
            for idx in range(top):
                _count += '{}\t{}\t{}\t{}\t{}\t{}'.format(
                    idx+1, _clist1[0][idx], _clist1[1][idx], idx+1,  _clist2[0][idx], _clist2[1][idx]
                )
                if idx < top-1:
                    _count += '\n'
            return [_date, _old, _count]
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None


if __name__ == '__main__':
    import pyperclip
    today = strftime("%Y-%m-%d", localtime())
    ccl = Ccl()
    ini = Ini()
    _year = ini.read('CCL', 'YEAR')
    if not re.match(r'\d{4}', _year):
        _year = '2009'
    while True:
        pyperclip.copy(today)
        date = input('请输入日期（默认今天的日期，可黏贴）：')
        if not re.match(r'\d{4}-\d{2}-\d{2}', date):
            print('输入日期异常，重新开始！')
            continue
        try:
            recv = ccl.get(date, show=True, year=_year)
            pyperclip.copy(recv[2])
            print('数据已复制到剪切板')
        except Exception as e:
            print('数据异常')
            _ = e
