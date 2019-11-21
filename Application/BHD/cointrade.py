#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib import request
from traceback import format_exc


class CoinTrade(object):
    __coin_list = ['BHD', 'LHD', 'BURST', 'BOOM', 'QT']

    def __init__(self):
        self.trade = {}

    @staticmethod
    def __symbol_trade(symbol):
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 '
                'QQBrowser/10.5.3819.400'
            )
        }
        if symbol == 'BOOM' or symbol == 'BURST' or symbol == 'QT':
            headers['Host'] = 'www.qbtc.ink'
            if symbol == 'BOOM':
                market = 'QT'
            else:
                market = 'CNYT'
            url = 'http://www.qbtc.ink/json/depthTable.do?tradeMarket={}&symbol={}'.format(market, symbol)
        elif symbol == 'BHD':
            url = 'https://api.aex.zone/depth.php?c={}&mk_type=cnc'.format(symbol)
        else:  # symbol == 'LHD':
            url = 'https://openapi.bitmart.io/v2/ticker?symbol={}_BHD'.format(symbol)
        _request = request.Request(url=url, headers=headers)
        try:
            _respond = request.urlopen(_request, timeout=5)
            context = _respond.read().decode('utf-8')
            context = json.loads(context)
            if symbol == 'BOOM' or symbol == 'BURST' or symbol == 'QT':
                data_list = [float(context['result']['buy'][0]['price']), float(context['result']['sell'][0]['price'])]
            elif symbol == 'BHD':
                data_list = [float(context['bids'][0][0]), float(context['asks'][0][0])]
            else:  # symbol == 'LHD':
                data_list = [float(context['bid_1']), float(context['ask_1'])]
            return data_list
        except Exception as e:
            print('get {} price\n{}\n{}'.format(symbol, e, format_exc()))
        return None

    def do_get_trade(self):
        _trade = {}
        for symbol in self.__coin_list:
            _data = self.__symbol_trade(symbol)
            if _data is not None:
                _trade[symbol] = _data
        if 'BOOM' in _trade.keys() and 'QT' in _trade.keys():
            _trade['BOOM'] = [_trade['BOOM'][0] * _trade['QT'][0], _trade['BOOM'][1] * _trade['QT'][1]]
        for coin in _trade.keys():
            if coin == 'QT':
                continue
            self.trade[coin] = _trade[coin]
        return self.trade


if __name__ == '__main__':
    ct = CoinTrade()
    print(ct.do_get_trade())
