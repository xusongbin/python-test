#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from time import time, strftime, localtime, mktime, strptime, sleep
from traceback import format_exc

from uupool import UUPool
from onepool import ONEPool
from cointrade import CoinTrade
from dingpost import DingPost


def write_log(_str):
    _data = strftime("%Y-%m-%d %H:%M:%S", localtime())
    _data += '.%03d ' % (int(time() * 1000) % 1000)
    _data += _str
    try:
        print(_data)
        with open('out.log', 'a+') as f:
            f.write(_data + '\n')
            f.flush()
    except Exception as e:
        print('{}\n{}'.format(e, format_exc()))


class Pool(object):
    uupool = UUPool()
    onepool = ONEPool()
    cointrade = CoinTrade()
    dingpost = DingPost()

    update_uupool = None
    update_onepool = None
    update_cointrade = None

    update_list = None

    def __init__(self):
        # 线程获取矿池数据，1小时获取一次，获取失败则10秒后重试
        self.thread_uupool = threading.Thread(target=self.on_thread_uupool)
        self.thread_uupool.setDaemon(True)
        self.thread_uupool.start()
        self.thread_onepool = threading.Thread(target=self.on_thread_onepool)
        self.thread_onepool.setDaemon(True)
        self.thread_onepool.start()
        self.thread_cointrade = threading.Thread(target=self.on_thread_cointrade)
        self.thread_cointrade.setDaemon(True)
        self.thread_cointrade.start()

        self.run()

    def on_thread_uupool(self):
        _timeout = 1 * 3600
        _tms = time() - _timeout
        while True:
            sleep(10)
            if (time() - _tms) < _timeout:
                continue
            _tms = time()
            self.update_uupool = self.uupool.do_update()
            print(self.update_uupool)

    def on_thread_onepool(self):
        _timeout = 1 * 3600
        _tms = time() - _timeout
        while True:
            sleep(10)
            if (time() - _tms) < _timeout:
                continue
            _tms = time()
            self.update_onepool = self.onepool.do_update()
            print(self.update_onepool)

    def on_thread_cointrade(self):
        _timeout = 1 * 3600
        _tms = time() - _timeout
        while True:
            sleep(10)
            if (time() - _tms) < _timeout:
                continue
            _tms = time()
            self.update_cointrade = self.cointrade.do_get_trade()
            print(self.update_cointrade)

    def run(self):
        while True:
            sleep(10)
            if self.update_onepool is None:
                continue
            if 'earning' not in self.update_onepool.keys():
                continue
            if 'assets' not in self.update_onepool.keys():
                continue
            if self.update_uupool is None:
                continue
            if 'earning' not in self.update_uupool.keys():
                continue
            if 'assets' not in self.update_uupool.keys():
                continue
            if self.update_cointrade is None:
                continue
            _coin_list = ['BHD', 'LHD', 'BOOM', 'BURST']
            _today = strftime("%Y-%m-%d", localtime())
            _update_list = []
            _pool_assert_value = 0
            _pool_today_value = 0
            for _coin in _coin_list:
                _coin_bid = float(self.update_cointrade[_coin][0])
                _coin_ask = float(self.update_cointrade[_coin][1])
                _coin_day = 0
                if _coin in self.update_uupool['earning'].keys():
                    if _today in self.update_uupool['earning'][_coin].keys():
                        _coin_day += float(self.update_uupool['earning'][_coin])
                if _coin in self.update_onepool['earning'].keys():
                    if _today in self.update_onepool['earning'][_coin].keys():
                        _coin_day += float(self.update_onepool['earning'][_coin])
                _coin_assert = 0
                if _coin in self.update_uupool['assets'].keys():
                    _coin_assert += float(self.update_uupool['assets'][_coin])
                if _coin in self.update_onepool['assets'].keys():
                    _coin_assert += float(self.update_onepool['assets'][_coin])
                _coin_day_value = _coin_day * _coin_bid
                _coin_assert_value = _coin_assert * _coin_bid
                _update_list.append(_coin_bid)
                _update_list.append(_coin_ask)
                _update_list.append(_coin_day)
                _update_list.append(_coin_day_value)
                _update_list.append(_coin_assert)
                _update_list.append(_coin_assert_value)
                _pool_assert_value += _coin_assert_value
                _pool_today_value += _coin_day_value
            _update_list.append(_pool_assert_value)
            _update_list.append(_pool_today_value)
            _power_rate = 1.3
            _power_pow = 210
            _power_value = _power_pow * 24 * 30 * 1.3 / 1000
            _update_list.append(_power_rate)
            _update_list.append(_power_pow)
            _update_list.append(_power_value)
            if self.update_list != _update_list:
                self.update_list = _update_list
                self.dingpost.post_md_list(_update_list)


if __name__ == '__main__':
    app = Pool()
