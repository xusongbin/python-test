#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from urllib import request
from urllib import parse
from hashlib import md5
from time import time

from md_logging import *

setup_log()
write_log = logging.getLogger('AEX_RESTFUL')


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
        try:
            with open('Aex.log', 'r') as f:
                key = json.load(f)
            self.access_key = key['Access_key']
            self.secret_key = key['Secret_key']
            self.account_id = key['Account_id']
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        write_log.debug('Key:{} Skey:{} Id:{}'.format(self.access_key, self.secret_key, self.account_id))

    def do_md5(self, ts):
        try:
            un_str = '{}_{}_{}_{}'.format(self.access_key, self.account_id, self.secret_key, ts)
            lw_str = parse.quote(un_str).lower()
            encryptor = md5()
            encryptor.update(lw_str.encode())
            en_str = encryptor.hexdigest()
            return en_str
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return ''

    # 返回自己當前的賬戶余額，包含系統支持的所有幣種。
    def do_get_mybalance(self):
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
            if re.match(r'\d+\.\d+\.\d+\.\d+ is not allowed', resp):
                write_log.error(resp)
                return {}
            data = json.loads(resp)
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 返回最高、最低交易行情和交易量，每15秒鐘更新
    def do_get_ticker(self, coin='bhd', kind='cnc'):
        url = 'https://api.aex.zone/ticker.php?c={}&mk_type={}'.format(coin, kind)
        try:
            req = request.Request(url, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 返回當前市場深度（委托掛單），其中 asks 是委賣單, bids 是委買單。返回30條。
    def do_get_depth(self, coin='bhd', kind='cnc'):
        url = 'https://api.aex.zone/depth.php?c={}&mk_type={}'.format(coin, kind)
        try:
            req = request.Request(url, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 返回系統支持的歷史成交記錄，返回最新30條。
    def do_get_trades(self, coin='bhd', kind='cnc', more=False):
        url = 'https://api.aex.zone/trades.php?c={}&mk_type={}{}'.format(coin, kind, ('&tid=100' if more else ''))
        try:
            req = request.Request(url, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 進行系統支持的所有數字貨幣的買賣操作。
    def do_submit_order(self, price, amount, _type=1, coinname='bhd', mk_type='cnc'):
        # 提交參數名	    描述
        # type          1為買入掛單，2為賣出掛單，不可為空
        # mk_type       交易區類型，必須為"btc|usdt|bitcny|cnc"其中之一，如"cnc", 不能為空
        # price         價格，btc定價最多8位小數，不同幣種有所不同，以網站顯示為準
        # amount        數量，最多6位小數
        # coinname      幣名，比如BTC、DOGE、BTS
        # 返回參數名	    描述
        # succ	        掛單成功
        # succ|123	    掛單成功，123為您掛單的ID
        # overBalance	賬戶余額不足
        #               其它返回表示不同的錯誤，情況太多，暫不羅列
        url = 'https://api.aex.zone/submitOrder.php'
        ts = int(time())
        en_str = self.do_md5(ts)
        data = {
            'key': self.access_key,
            'time': ts,
            'md5': en_str,
            'type': _type,
            'mk_type': mk_type,
            'price': price,
            'amount': amount,
            'coinname': coinname
        }
        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, headers=self.headers, data=data)
            resp = request.urlopen(req).read().decode('utf-8')
            data = resp
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 進行自己委單的撤銷操作。
    def do_cancel_order(self, order_id, coinname='bhd', mk_type='cnc'):
        # 提交參數名	    描述
        # order_id      要撤的單的ID
        # mk_type       交易區類型，必須為"btc|usdt|bitcny|cnc"其中之一，如"cnc", 不能為空
        # coinname      幣名，比如BTC、DOGE、BTS
        # 返回參數名	    描述
        # succ	        撤單成功
        # overtime      該單不存在，或者已成交了
        url = 'https://api.aex.zone/cancelOrder.php'
        ts = int(time())
        en_str = self.do_md5(ts)
        data = {
            'key': self.access_key,
            'time': ts,
            'md5': en_str,
            'order_id': order_id,
            'mk_type': mk_type,
            'coinname': coinname
        }
        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, headers=self.headers, data=data)
            resp = request.urlopen(req).read().decode('utf-8')
            data = resp
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 返回自己當前沒有成交的委單,已成交的掛單會顯示在成交記錄中。
    def do_get_orderlist(self, coinname='bhd', mk_type='cnc'):
        # 提交參數名	    描述
        # mk_type       交易區類型，必須為"btc|usdt|bitcny|cnc"其中之一，如"cnc", 不能為空
        # coinname      幣名，比如BTC、DOGE、BTS
        # 返回參數名	    描述
        # 掛單為空		[]
        # 掛單不為空
        # [{"id":"123", "type":"1", "coinname":"BTC", "order_amount":"23.232323", "order_price":"0.2929"},
        # {"id":"123", "type":"1", "coinname":"LTC","order_amount":"23.232323", "order_price":"0.2929"}]
        url = 'https://api.aex.zone/getOrderList.php'
        ts = int(time())
        en_str = self.do_md5(ts)
        data = {
            'key': self.access_key,
            'time': ts,
            'md5': en_str,
            'mk_type': mk_type,
            'coinname': coinname
        }
        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, headers=self.headers, data=data)
            resp = request.urlopen(req).read().decode('utf-8')
            data = resp
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}

    # 返回自己的歷史成交記錄，每頁顯示30條。
    def do_get_tradelist(self, page=1, coinname='bhd', mk_type='cnc'):
        # 提交參數名	    描述
        # mk_type       交易區類型，必須為"btc|usdt|bitcny|cnc"其中之一，如"cnc", 不能為空
        # coinname      幣名，比如BTC、DOGE、BTS
        # page          翻頁，0為第1頁，每頁30條，不填則默認為第1頁
        # 返回參數名	    描述
        # 為空		    []
        # 不為空
        # {id:123,buyer_id:123,seller_id:123,volume:123,price:123,coinname:"btc",time:"1990-02-22 12:12:12"}
        url = 'https://api.aex.zone/getMyTradeList.php'
        ts = int(time())
        en_str = self.do_md5(ts)
        data = {
            'key': self.access_key,
            'time': ts,
            'md5': en_str,
            'mk_type': mk_type,
            'coinname': coinname,
            'page': page
        }
        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, headers=self.headers, data=data)
            resp = request.urlopen(req).read().decode('utf-8')
            data = resp
            return data
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return {}


if __name__ == '__main__':
    aex = Aex()
    print(aex.do_get_mybalance())
    # print(aex.do_get_ticker())
    # print(aex.do_get_depth())
    # print(aex.do_get_trades())

    # print(aex.do_submit_order(100, 1))
    # print(aex.do_cancel_order(516384))
    # print(aex.do_get_orderlist())
    # print(aex.do_get_tradelist())

