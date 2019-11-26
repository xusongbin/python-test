#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import threading
from urllib import request
from time import time, strftime, localtime, sleep

from traceback import format_exc


class UUPool(object):
    __token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE3Nzc4MTY2ODMwIiwidGltZXN0YW1wIjoxNTc0Nzc3OTUxMDU4LCJ1aWQiOjEwNjk5LCJhY2NvdW50S2V5IjoiMDg2OGRiZTItZDU5MS0zM2MxLWJlYjItZjZkZDUwYmRiNzJlIiwiZXhwIjoxNTc0ODY0MzUxLCJuYmYiOjE1NzQ3Nzc5NTF9.Iy7IJ-o_ljBAL6is3dA_Ib_TkG2tX-ON3dOn3mwv2ro'
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

    def __init__(self, period=3600, timeout=5):
        self.period = period
        self.timeout = timeout

        self.pool_coin = ['BHD', 'LHD']
        self.pool_property = {
            'assert': {
                'time': time() - period,
                'BHD': {'valid': False, 'amount': 0.0},
                'LHD': {'valid': False, 'amount': 0.0},
            },
            'earnings': {
                'BHD': {'valid': False, 'time': time() - period, 'today': 0.0, 'average': 0.0},
                'LHD': {'valid': False, 'time': time() - period, 'today': 0.0, 'average': 0.0},
            }
        }
        for coin in self.pool_coin:
            self.pool_property['assert'][coin] = {'valid': False, 'amount': 0.0}
            self.pool_property['earnings'][coin] = {
                'valid': False, 'time': time() - period, 'today': 0.0, 'average': 0.0}

        self.thread_pool = threading.Thread(target=self.on_thread_pool)
        self.thread_pool.setDaemon(True)
        self.thread_pool.start()

    def get_property(self):
        _coin_list = []
        _property_valid = True
        _property_coin = {}
        for coin in self.pool_coin:
            _coin_list.append(coin)
            if not self.pool_property['assert'][coin]['valid']:
                _property_valid = False
            if not self.pool_property['earnings'][coin]['valid']:
                _property_valid = False
            _property_coin[coin] = {
                'today': self.pool_property['earnings'][coin]['today'],
                'average': self.pool_property['earnings'][coin]['average'],
                'amount': self.pool_property['assert'][coin]['amount']
            }
        _property = dict({'valid': _property_valid, 'coin': _coin_list}, **_property_coin)
        return _property

    def check_timeout(self, ts):
        if time() - ts >= self.period:
            return True
        return False

    def get_timeout(self, dl=None):
        if dl:
            return time() - self.period + dl
        else:
            return time()

    def on_thread_pool(self):
        last_date = ''
        while True:
            sleep(1)
            this_date = strftime("%Y-%m-%d", localtime())
            if last_date != this_date:
                last_date = this_date
                self.pool_property['assert']['time'] = self.get_timeout(self.timeout)
                self.pool_property['earnings']['time'] = self.get_timeout(self.timeout)
            if self.check_timeout(self.pool_property['assert']['time']):
                assets = self.do_get_assets()
                self.do_parse_assets(assets)
            for coin in self.pool_coin:
                if self.check_timeout(self.pool_property['earnings'][coin]['time']):
                    earnings = self.do_get_earnings(coin)
                    self.do_parse_earnings(coin, earnings)

    def do_parse_assets(self, assets):
        _count = 0
        for coin in self.pool_coin:
            if coin in assets.keys():
                _count += 1
                self.pool_property['assert'][coin]['amount'] = assets[coin]
                self.pool_property['assert'][coin]['valid'] = True
                print('PARSE {} ASSERT: {}'.format(coin, assets[coin]))
        if _count == len(self.pool_coin):
            self.pool_property['assert']['time'] = self.get_timeout()
        else:
            self.pool_property['assert']['time'] = self.get_timeout(self.timeout)

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
                _resp_dict[data['coinName'].upper()] = float(data['availableAsset'])
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        # print(_resp_dict)
        return _resp_dict

    def do_parse_earnings(self, coin, earnings):
        today_date = strftime("%Y-%m-%d", localtime())
        total_day = 0
        total_amount = 0
        if earnings:
            if today_date in earnings.keys():
                self.pool_property['earnings'][coin]['today'] = earnings[today_date]
            else:
                self.pool_property['earnings'][coin]['today'] = 0
            for day in earnings.keys():
                if day == today_date:
                    continue
                total_day += 1
                total_amount += earnings[day]
            if total_day == 0:
                self.pool_property['earnings'][coin]['average'] = 0
            else:
                self.pool_property['earnings'][coin]['average'] = total_amount / total_day
            self.pool_property['earnings'][coin]['valid'] = True
            self.pool_property['earnings'][coin]['time'] = self.get_timeout()
            _property = self.pool_property['earnings'][coin]
            print('PARSE {} EARNINGS: today:{} average:{}'.format(coin, _property['today'], _property['average']))
        else:
            self.pool_property['earnings'][coin]['time'] = self.get_timeout(self.timeout)

    def do_get_earnings(self, coin):
        _resp_dict = {}
        _url = 'https://uupool.com/v1/earnings/days/?pageSize=10&page=1&coin_name={}&type=0'.format(coin)
        _request = request.Request(_url, headers=self.headers)
        try:
            _respond = request.urlopen(_request, timeout=5)
            _respond = _respond.read().decode('utf-8')
            _content = json.loads(_respond)
            # print(_content)
            for data in _content['data']['records']:
                _resp_dict[data['date']] = float(data['totalIncome'])
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        # print(_resp_dict)
        return _resp_dict


if __name__ == '__main__':
    pool = UUPool()
    while True:
        pass
