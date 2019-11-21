#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gzip
from urllib import request
from urllib import parse
from lxml import etree
from time import time, strftime, localtime, mktime, strptime, sleep

from traceback import format_exc


class ONEPool(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': (
            'language=zh-CN; '
            'loginName=mark3333520%40163.com; '
            'loginPwd=f3in2oWmp61%2FdHqnfanUzo6oqWKMjKnOl4h%2B'
            'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
            'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
            'pZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf; '
            'sd7038915=o58htabrp06ufak7re61gum174;'
        ),
        'Host': 'www.onepool.co',
        'Origin': 'http://www.onepool.co',
        'Referer': 'http://www.onepool.co/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': (
                'Mozilla/5.0 '
                '(Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 '
                '(KHTML, like Gecko) '
                'Chrome/70.0.3538.25 '
                'Safari/537.36 Core/1.70.3722.400 '
                'QQBrowser/10.5.3738.400'
            )
    }

    def __init__(self):
        self.data_storage = {}

    def do_update(self):
        _assets = self.do_get_assets()
        if _assets:
            self.data_storage['assets'] = _assets
        _earning = self.do_get_earnings()
        if _earning:
            self.data_storage['earning'] = _earning
        print(self.data_storage)
        return self.data_storage

    def do_get_assets(self):
        _resp_dict = {}
        _url = 'https://www.onepool.co/home/user/asset.html'
        _request = request.Request(_url, headers=self.headers)
        try:
            _respond = request.urlopen(_request)
            _content = _respond.read()
            if _respond.info().get('Content-Encoding') == 'gzip':
                _content = gzip.decompress(_content).decode('utf-8')
            else:
                _content = _content.decode('utf-8')
            # print(_content)
            html = etree.HTML(_content)
            _property = {}
            _matters = {}
            for tr in html.xpath('//div[@class="layui-tab-content"]/div[1]/div/table/tbody/tr'):
                coin_name = tr.xpath('td[1]/text()')[1].strip().split(' ')[0].upper()
                _property[coin_name] = float(tr.xpath('td[4]/text()')[0])
            for tr in html.xpath('//div[@class="layui-tab-content"]/div[2]/div/table/tbody/tr'):
                coin_name = tr.xpath('td[1]/text()')[1].strip().split(' ')[0].upper()
                _matters[coin_name] = float(tr.xpath('td[2]/text()')[0]) + float(tr.xpath('td[4]/text()')[0])
            for coin in _property.keys():
                _resp_dict[coin] = _property[coin]
                if coin in _matters.keys():
                    _resp_dict[coin] += _matters[coin]
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        # print(_resp_dict)
        return _resp_dict

    def do_get_earnings(self):
        _resp_dict = {}
        _coin_list = ['BHD', 'LHD', 'BOOM', 'HDD', 'BURST']
        for _coin in _coin_list:
            _resp_dict[_coin] = self.do_get_days(_coin)
        # print(_resp_dict)
        return _resp_dict

    def do_get_days(self, coin):
        _resp_dict = {}
        _coin_type = {'BHD': 'eco_bhd', 'HDD': 'eco_hdd', 'LHD': 'eco_lhd', 'BOOM': 'boom', 'BURST': 'burst'}
        _url = 'https://www.onepool.co/{}/user/getincomeinquiry.html'.format(_coin_type[coin.upper()])
        _stop_ts = int(time() / 86400) * 86400
        _start_ts = _stop_ts - 86400 * 10
        _stop = strftime("%Y-%m-%d", localtime(_stop_ts))
        _start = strftime("%Y-%m-%d", localtime(_start_ts))
        data = {'page': 1, 'start': _start, 'stop': _stop}
        data = parse.urlencode(data).encode('utf-8')
        _request = request.Request(_url, data=data, headers=self.headers)
        try:
            _respond = request.urlopen(_request, timeout=5)
            _respond = _respond.read().decode('utf-8')
            _content = json.loads(_respond)
            # print(_content)
            for data in _content['data']['data']:
                _resp_dict[data['profit_date']] = data['amount']
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        # print(_resp_dict)
        return _resp_dict


if __name__ == '__main__':
    pool = ONEPool()
    # pool.do_get_assets()
    # pool.do_get_days('bhd')
    # pool.do_get_earnings()
    pool.do_update()
