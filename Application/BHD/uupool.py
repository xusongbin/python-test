#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib import request

from traceback import format_exc


class UUPool(object):
    __token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE3Nzc4MTY2ODMwIiwidGltZXN0YW1wIjoxNTc0NTIwNjg3MzU1LCJ1aWQiOjEwNjk5LCJhY2NvdW50S2V5IjoiMDg2OGRiZTItZDU5MS0zM2MxLWJlYjItZjZkZDUwYmRiNzJlIiwiZXhwIjoxNTc0NjA3MDg3LCJuYmYiOjE1NzQ1MjA2ODd9.Ro-ddvqsNqrbLipmQpRj-YiaqvIbr-T2XL4WB9Bm2pU'
    headers = {
        'authorization_token': __token,
        'authorization_uid': '10699',
        'authorization_username': '17778166830',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=utf-8',
        'Cookie': (
            '__tins__20396121=%7B%22sid%22%3A%201574256862961'
            '%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%'
            '201574258662961%7D; __51cke__=; __51laig__=1'
        ),
        'Host': 'uupool.com',
        'lan': 'zh',
        'platform': 'pc',
        'Referer': 'https://uupool.com/asset',
        'token': __token,
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 6.1; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 '
            'QQBrowser/10.5.3819.400'
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
        # print(self.data_storage)
        return self.data_storage

    def do_get_assets(self):
        _resp_dict = {}
        _url = 'https://uupool.com/v1/assets/all'
        _request = request.Request(_url, headers=self.headers)
        try:
            _respond = request.urlopen(_request, timeout=5)
            _respond = _respond.read().decode('utf-8')
            _content = json.loads(_respond)
            # print(_content)
            for data in _content['data']:
                _resp_dict[data['coinName'].upper()] = data['availableAsset']
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        # print(_resp_dict)
        return _resp_dict

    def do_get_earnings(self):
        _resp_dict = {}
        _coin_list = ['BHD', 'LHD']
        for _coin in _coin_list:
            _resp_dict[_coin] = self.do_get_days(_coin)
        # print(_resp_dict)
        return _resp_dict

    def do_get_days(self, coin):
        _resp_dict = {}
        _url = 'https://uupool.com/v1/earnings/days/?pageSize=10&page=1&coin_name={}&type=0'.format(coin)
        _request = request.Request(_url, headers=self.headers)
        try:
            _respond = request.urlopen(_request, timeout=5)
            _respond = _respond.read().decode('utf-8')
            _content = json.loads(_respond)
            # print(_content)
            for data in _content['data']['records']:
                _resp_dict[data['date']] = data['totalIncome']
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        # print(_resp_dict)
        return _resp_dict


if __name__ == '__main__':
    pool = UUPool()
    # pool.do_get_assets()
    # pool.do_get_days('bhd')
    # pool.do_get_earnings()
    print(pool.do_update())
