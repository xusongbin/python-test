#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gzip
import threading
import requests
from lxml import etree
from time import time, strftime, localtime, sleep

from traceback import format_exc

import gc
gc.set_threshold(50, 10, 10)
gc.enable()


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

    def __init__(self, period=3600, timeout=5):
        self.period = period
        self.timeout = timeout

        self.pool_coin = ['BURST', 'BOOM']
        self.pool_property = {
            'assert': {
                'time': time() - period,
                'BURST': {'valid': False, 'amount': 0.0},
                'BOOM': {'valid': False, 'amount': 0.0},
            },
            'earnings': {
                'BURST': {'valid': False, 'time': time() - period, 'today': 0.0, 'average': 0.0},
                'BOOM': {'valid': False, 'time': time() - period, 'today': 0.0, 'average': 0.0},
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
        _url = 'https://www.onepool.co/home/user/asset.html'
        try:
            _respond = requests.get(_url, headers=self.headers, timeout=3)
            html = etree.HTML(_respond.text)
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
        _coin_type = {'BHD': 'eco_bhd', 'HDD': 'eco_hdd', 'LHD': 'eco_lhd', 'BOOM': 'boom', 'BURST': 'burst'}
        _url = 'https://www.onepool.co/{}/user/getincomeinquiry.html'.format(_coin_type[coin.upper()])
        _stop_ts = int(time() / 86400) * 86400
        _start_ts = _stop_ts - 86400 * 10
        _stop = strftime("%Y-%m-%d", localtime(_stop_ts))
        _start = strftime("%Y-%m-%d", localtime(_start_ts))
        data = {'page': 1, 'start': _start, 'stop': _stop}
        try:
            _respond = requests.post(_url, data=data, headers=self.headers, timeout=3)
            _content = _respond.json()
            for data in _content['data']['data']:
                _resp_dict[data['profit_date']] = float(data['amount'])
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return _resp_dict


if __name__ == '__main__':
    pool = ONEPool(1)
    while True:
        pass
