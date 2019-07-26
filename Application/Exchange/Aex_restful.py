#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from urllib import request
from urllib import parse
from hashlib import md5
from time import time

import traceback
from md_logging import Logging


class Aex(object):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 6.1; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/70.0.3538.25 '
            'Safari/537.36 Core/1.70.3719.400 '
            'QQBrowser/10.5.3715.400'
        )
    }

    def __init__(self):
        self.access_key = ''
        self.secret_key = ''
        self.account_id = 0
        self.log = Logging('AEX')
        try:
            with open('Aex.log', 'r') as f:
                key = json.load(f)
            self.access_key = key['Access_key']
            self.secret_key = key['Secret_key']
            self.account_id = key['Account_id']
        except Exception as e:
            self.log.error('{}\n{}'.format(e, traceback.format_exc()))
        self.log.debug('Key:{} Skey:{} Id:{}'.format(self.access_key, self.secret_key, self.account_id))

    def do_md5(self, ts):
        try:
            un_str = '{}_{}_{}_{}'.format(self.access_key, self.account_id, self.secret_key, ts)
            lw_str = parse.quote(un_str).lower()
            encryptor = md5()
            encryptor.update(lw_str.encode())
            en_str = encryptor.hexdigest()
            return en_str
        except Exception as e:
            self.log.error('{}\n{}'.format(e, traceback.format_exc()))
        return ''

    def do_get_mybalance(self):
        # 返回自己當前的賬戶余額，包含系統支持的所有幣種。
        url = 'https://api.aex.zone/getMyBalance.php'
        ts = int(time())
        en_str = self.do_md5(ts)
        data = {
            'key': self.access_key,
            'time': ts,
            'md5': en_str
        }
        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, headers=self.headers, data=data)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            self.log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    def do_get_ticker(self, coin='bhd', kind='cnc'):
        # 返回最高、最低交易行情和交易量，每15秒鐘更新
        url = 'https://api.aex.zone/ticker.php?c={}&mk_type={}'.format(coin, kind)
        try:
            req = request.Request(url, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            self.log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    def do_get_depth(self, coin='bhd', kind='cnc'):
        # 返回當前市場深度（委托掛單），其中 asks 是委賣單, bids 是委買單。返回30條。
        url = 'https://api.aex.zone/depth.php?c={}&mk_type={}'.format(coin, kind)
        try:
            req = request.Request(url, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            self.log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    def do_get_trades(self, coin='bhd', kind='cnc', more=False):
        # 返回系統支持的歷史成交記錄，返回最新30條。
        url = 'https://api.aex.zone/trades.php?c={}&mk_type={}{}'.format(coin, kind, ('&tid=100' if more else ''))
        try:
            req = request.Request(url, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            self.log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}


if __name__ == '__main__':
    aex = Aex()
    # print(aex.do_get_mybalance())
    # print(aex.do_get_ticker())
    # print(aex.do_get_depth())
    print(aex.do_get_trades())
