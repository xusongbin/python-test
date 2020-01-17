#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import threading
import requests
from time import time, sleep, strftime, localtime
from traceback import format_exc

import gc
gc.set_threshold(50, 10, 10)
gc.enable()


class CoinTrade(object):
    def __init__(self, period=3600, timeout=5, debug=False):
        self.period = period
        self.timeout = timeout

        self.coin_list = ['BHD', 'LHD', 'USDT', 'QT', 'BURST', 'BOOM']
        self.coin_trade = {
            'BHD': {'valid': False, 'time': time() - period, 'bid': 0.0, 'ask': 0.0}
        }
        for coin in self.coin_list:
            self.coin_trade[coin] = {'valid': False, 'time': time() - period, 'bid': 0.0, 'ask': 0.0}

        self.thread_trade = threading.Thread(target=self.on_thread_trade)
        self.thread_trade.setDaemon(True)

        if not debug:
            self.thread_trade.start()

    def get_trade(self):
        _trade = {}
        _trade_valid = True
        for coin in self.coin_list:
            if not self.coin_trade[coin]['valid']:
                _trade_valid = False
            _trade[coin] = {'bid': self.coin_trade[coin]['bid'], 'ask': self.coin_trade[coin]['ask']}
        _trade['valid'] = _trade_valid
        return _trade

    def check_timeout(self, ts):
        if (time() - ts) >= self.period:
            return True
        return False

    def get_timeout(self, dl=None):
        if dl:
            return time() - self.period + dl
        else:
            return time()

    def on_thread_trade(self):
        while True:
            sleep(1)
            for coin in self.coin_list:
                if self.check_timeout(self.coin_trade[coin]['time']):
                    # print('PARSE {} TRADE TIMEOUT:{}'.format(coin, strftime("%Y-%m-%d %H:%M:%S", localtime())))
                    trade = self.get_symbol_trade(coin)
                    self.prase_symbol_trade(coin, trade)

    def prase_symbol_trade(self, coin, trade):
        if trade:
            if coin == 'LHD' and not self.coin_trade['BHD']['valid']:
                self.coin_trade[coin]['time'] = self.get_timeout(self.timeout)
                return
            if coin == 'BOOM' and not self.coin_trade['QT']['valid']:
                self.coin_trade[coin]['time'] = self.get_timeout(self.timeout)
                return
            if coin == 'BURST' and not self.coin_trade['USDT']['valid']:
                self.coin_trade[coin]['time'] = self.get_timeout(self.timeout)
                return
            if coin == 'QT' and not self.coin_trade['USDT']['valid']:
                self.coin_trade[coin]['time'] = self.get_timeout(self.timeout)
                return
            self.coin_trade[coin]['bid'] = trade[0]
            self.coin_trade[coin]['ask'] = trade[1]
            if coin == 'QT':
                self.coin_trade[coin]['bid'] = trade[0] * self.coin_trade['USDT']['bid']
                self.coin_trade[coin]['ask'] = trade[1] * self.coin_trade['USDT']['ask']
            if coin == 'LHD':
                self.coin_trade[coin]['bid'] = trade[0] * self.coin_trade['BHD']['bid']
                self.coin_trade[coin]['ask'] = trade[1] * self.coin_trade['BHD']['ask']
            if coin == 'BOOM':
                self.coin_trade[coin]['bid'] = trade[0] * self.coin_trade['QT']['bid']
                self.coin_trade[coin]['ask'] = trade[1] * self.coin_trade['QT']['ask']
            if coin == 'BURST':
                self.coin_trade[coin]['bid'] = trade[0] * self.coin_trade['USDT']['bid']
                self.coin_trade[coin]['ask'] = trade[1] * self.coin_trade['USDT']['ask']
            self.coin_trade[coin]['valid'] = True
            self.coin_trade[coin]['time'] = self.get_timeout()
            _trade = self.coin_trade[coin]
            print('PARSE {} TRADE: BID:{} ASK:{}'.format(coin, _trade['bid'], _trade['ask']))
        else:
            self.coin_trade[coin]['time'] = self.get_timeout(self.timeout)

    @staticmethod
    def get_symbol_trade(symbol):
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 '
                'QQBrowser/10.5.3819.400'
            )
        }
        symbol = symbol.upper()
        if symbol == 'BOOM' or symbol == 'BURST' or symbol == 'USDT' or symbol == 'QT':
            headers['Host'] = 'www.qbtc.ink'
            if symbol == 'BOOM':
                market = 'QT'
            elif symbol == 'BURST' or symbol == 'QT':
                market = 'USDT'
            else:
                market = 'CNYT'
            url = 'http://www.qbtc.ink/json/depthTable.do?tradeMarket={}&symbol={}'.format(market, symbol)
        elif symbol == 'BHD':
            url = 'https://api.aex.zone/depth.php?c={}&mk_type=cnc'.format(symbol)
        else:  # symbol == 'LHD':
            url = 'https://openapi.bitmart.io/v2/ticker?symbol={}_BHD'.format(symbol)
        try:
            _respond = requests.get(url=url, headers=headers, timeout=2)
            context = _respond.json()
            if symbol == 'BOOM' or symbol == 'BURST' or symbol == 'QT' or symbol == 'USDT':
                data_list = [float(context['result']['buy'][0]['price']), float(context['result']['sell'][0]['price'])]
            elif symbol == 'BHD':
                data_list = [float(context['bids'][0][0]), float(context['asks'][0][0])]
            else:  # symbol == 'LHD':
                data_list = [float(context['bid_1']), float(context['ask_1'])]
            return data_list
        except Exception as e:
            print('get {} price\n{}\n{}'.format(symbol, e, format_exc()))
        return None


if __name__ == '__main__':
    debug = False
    ct = CoinTrade(period=1, debug=debug)
    if not debug:
        while True:
            pass
    coin_price = ct.get_symbol_trade('BURST')
    print(coin_price)
