#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
import random
import requests
from urllib.parse import quote
from hashlib import md5
from time import time, strftime, localtime, mktime, strptime


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
        print('write log exception %s' % e)


class BitAtm(object):
    method_history_kline = '/market/history.kline'  # 历史K线
    method_detail_merged = '/market/detail.merged'  # 滚动24小时交易和最优报价聚合行情
    method_detail = '/market/detail'    # 滚动24小时交易聚合行情
    method_tickers = '/market/tickers'  # 全部symbol的交易行情
    method_depth = '/market/depth'      # 单个symbol市场深度行情
    method_trade = '/market/trade'      # 单个symbol最新成交记录
    method_rate = '/v1/common/rate'     # 汇率
    method_accounts = '/v1/account/accounts'    # 查询用户的所有账户状态
    method_balance = '/v1/account/balance'      # 查询指定账户余额
    method_order_create = '/v1/order/create'    # 下单
    method_order_cancel = '/v1/order/cancel'    # 撤销一个订单

    def __init__(self):
        self.access_key = ''
        self.secret_key = ''
        try:
            with open('BitATM.log', 'r') as f:
                key = json.load(f)
            self.access_key = key['Access_key']
            self.secret_key = key['Secret_key']
        except Exception as e:
            write_log('Load key except: %s' % e)
        self.type_name = 'Content-Type'
        self.type_get = 'application/x-www-form-urlencoded'
        self.type_post = 'application/json'
        self.url = 'https://open.bitatm.com'

    # 获取签名
    def get_signature(self, randstr, timestamp):
        signatue_key = 'accesskey={}&randstr={}&timestamp={}&secretkey={}'.format(
            self.access_key,
            randstr,
            timestamp,
            self.secret_key
        )
        url_str = quote(signatue_key).lower()
        url_byte = url_str.encode()
        md5_maker = md5()
        md5_maker.update(url_byte)
        signatue_str = md5_maker.hexdigest()
        return signatue_str

    # 获取历史K线
    def get_history_kline(self, periol, count, ):
        headers = {self.type_name: self.type_get}
        symbol = 'burstbhd'     # btcusdt,bchbtc,rcneth…
        # periol = '1min'     # 1min,5min,15min,30min,60min,1day,1week,1mon
        # count = '5'       # [1~1000]
        value = '?Symbol={}&Period={}&Size={}'.format(symbol, periol, count)
        resp = requests.get(self.url + self.method_history_kline + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        # print(cdict)
        for node in cdict['data']:
            print(
                '时间：{} 成交量：{:<10} 开盘价：{:.8f} 收盘价：{:.8f} 最低价：{:.8f} 最高价：{:.8f}'.format(
                    strftime("%Y-%m-%d %H:%M:%S", localtime(node['ts'])),
                    str(node['amount']),
                    node['open'],
                    node['close'],
                    node['low'],
                    node['high']
                )
            )

    # 滚动24小时交易和最优报价聚合行情
    def get_detail_merged(self):
        headers = {self.type_name: self.type_get}
        symbol = 'burstbhd'     # btcusdt,bchbtc,rcneth…
        value = '?Symbol={}'.format(symbol)
        resp = requests.get(self.url + self.method_detail_merged + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        print(cdict)

    def get_detail(self):
        headers = {self.type_name: self.type_get}
        symbol = 'burstbhd'     # btcusdt,bchbtc,rcneth…
        value = '?Symbol={}'.format(symbol)
        resp = requests.get(self.url + self.method_detail + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        print(cdict)

    def get_tickers(self):
        headers = {self.type_name: self.type_get}
        resp = requests.get(self.url + self.method_tickers, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        print(cdict)

    def get_depth(self):
        headers = {self.type_name: self.type_get}
        symbol = 'burstbhd'     # btcusdt,bchbtc,rcneth…
        value = '?Symbol={}'.format(symbol)
        resp = requests.get(self.url + self.method_depth + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        # print(cdict)
        depth = cdict['data']['asks']
        for dep in depth:
            if dep['id'] > 5:
                break
            print('卖方 单价：{:<15} 数量：{:<10}'.format(
                dep['price'],
                dep['amount']
            ))
        depth = cdict['data']['bids']
        for dep in depth:
            if dep['id'] > 5:
                break
            print('买方 单价：{:<15} 数量：{:<10}'.format(
                dep['price'],
                dep['amount']
            ))

    def get_trade(self):
        headers = {self.type_name: self.type_get}
        symbol = 'burstbhd'     # btcusdt,bchbtc,rcneth…
        value = '?Symbol={}'.format(symbol)
        resp = requests.get(self.url + self.method_trade + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        # print(cdict)
        node = cdict['data'][0]
        print(
            '时间：{} 成交量：{:<10} 成交价：{} {}'.format(
                strftime("%Y-%m-%d %H:%M:%S", localtime(node['ts'])),
                str(node['amount']),
                node['price'],
                '卖出' if node['direction'] < 0 else '买入'
            )
        )

    def get_rate(self):
        headers = {self.type_name: self.type_get}
        resp = requests.get(self.url + self.method_rate, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        print(cdict)

    def get_accounts(self):
        rand_str = ''.join(random.sample(string.ascii_letters, 10))
        timestamp = int(time() * 1000)
        headers = {self.type_name: self.type_get}
        signature = self.get_signature(rand_str, timestamp)
        value = '?AccessKey={}&RandStr={}&Timestamp={}&Signature={}'.format(
            self.access_key,
            rand_str,
            timestamp,
            signature
        )
        resp = requests.get(self.url + self.method_accounts + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        print(cdict)

    def get_balance(self):
        rand_str = ''.join(random.sample(string.ascii_letters, 10))
        timestamp = int(time() * 1000)
        headers = {self.type_name: self.type_get}
        signature = self.get_signature(rand_str, timestamp)
        value = '?AccessKey={}&RandStr={}&Timestamp={}&Signature={}'.format(
            self.access_key,
            rand_str,
            timestamp,
            signature
        )
        resp = requests.get(self.url + self.method_balance + value, headers=headers)
        context = resp.text
        cdict = json.loads(context)
        # print(cdict)
        balance = cdict['data']
        for bal in balance:
            print('币种：{:<8} 余额：{:<15} 冻结：{:<15}'.format(
                bal['currency'],
                bal['balance'],
                bal['frozen']
            ))


def main():
    ba = BitAtm()
    # ba.get_history_kline('1min', 5)
    ba.get_detail_merged()
    # ba.get_detail()
    # ba.get_tickers()
    # ba.get_depth()
    # ba.get_trade()
    # ba.get_rate()
    # ba.get_accounts()
    # ba.get_balance()


if __name__ == '__main__':
    main()
