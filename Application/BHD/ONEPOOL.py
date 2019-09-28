#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import gc
import json
import gzip
import threading
from urllib import request
from urllib import parse
from time import time, strftime, localtime, mktime, strptime, sleep
from contextlib import closing
from traceback import format_exc
gc.set_threshold(100, 10, 10)
gc.enable()

from lxml import etree


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
    user_agent = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
    )
    robot = (
        'https://oapi.dingtalk.com/robot/send?access_token='
        '7a45b3d175f5060361726500dab381992d0547bc185ae5d15eb5744ce70adbb1'
    )
    item = [
        'bhdBid', 'bhdAsk', 'hddBid', 'hddAsk', 'lhdBid', 'lhdAsk',
        'boomBid', 'boomAsk', 'burstBid', 'burstAsk',
        'poolProperty', 'poolToday', 'poolAverage',
        'bhdToday', 'bhdFuture', 'bhdDayinc', 'bhdAmount', 'bhdProperty',
        'hddToday', 'hddFuture', 'hddDayinc', 'hddAmount', 'hddProperty',
        'lhdToday', 'lhdFuture', 'lhdDayinc', 'lhdAmount', 'lhdProperty',
        'boomToday', 'boomFuture', 'boomDayinc', 'boomAmount', 'boomProperty',
        'burstToday', 'burstFuture', 'burstDayinc', 'burstAmount', 'burstProperty',
        'cycPrice', 'cycPow', 'cycPay',
        'cycMachine', 'cycDisk', 'cycCapacity',
        'cycIncome', 'cycProfit', 'cycMonth', 'cycDate'
    ]
    last_push_str = None
    last_push_dict = {}
    this_push_dict = {}
    this_push_direct = {}
    for key in item:
        last_push_dict[key] = 0.0
        this_push_dict[key] = 0.0
    for key in item:
        this_push_direct[key] = 'black'
    robot_tout = 60 * 60      # 上报频率60分钟一次
    robot_ts = time() - robot_tout
    template = 'property.md'

    cycMachine = 25000
    cycDisk = 16
    cycCapacity = 134
    cycPrice = 1.5
    cycPow = 200

    tradeBHD = 0
    tradeLHD = 0
    tradeHDD = 0
    tradeBOOM = 0
    tradeBURST = 0

    poolAverage = 0

    bhdToday = 0
    hddToday = 0
    lhdToday = 0
    boomToday = 0
    burstToday = 0
    bhdFuture = 0
    hddFuture = 0
    lhdFuture = 0
    boomFuture = 0
    burstFuture = 0
    bhdDayinc = 0
    hddDayinc = 0
    lhdDayinc = 0
    boomDayinc = 0
    burstDayinc = 0
    bhdAmount = 0
    hddAmount = 0
    lhdAmount = 0
    boomAmount = 0
    burstAmount = 0

    def __init__(self, test=False):
        if test:
            return
        # 线程获取挖财数据，720分钟获取一次，获取失败则5秒后重试
        self.thread_wacai = threading.Thread(target=self.on_thread_wacai)
        self.thread_wacai.setDaemon(True)
        self.thread_wacai.start()

        # 线程获取日均收益，120分钟获取一次，获取失败则5秒后重试
        self.thread_average = threading.Thread(target=self.on_thread_average)
        self.thread_average.setDaemon(True)
        self.thread_average.start()

        # 线程获取实时报价，40分钟获取一次，获取失败则5秒后重试
        self.thread_trade = threading.Thread(target=self.on_thread_trade)
        self.thread_trade.setDaemon(True)
        self.thread_trade.start()

        # 线程获取矿池资产，40分钟获取一次，获取失败则5秒后重试
        self.thread_property = threading.Thread(target=self.on_thread_property)
        self.thread_property.setDaemon(True)
        self.thread_property.start()

        # 线程获取当日收益，30分钟获取一次，获取失败则5秒后重试
        self.thread_today = threading.Thread(target=self.on_thread_today)
        self.thread_today.setDaemon(True)
        self.thread_today.start()

        # 上报数据
        self.run()

    def __get_valid_time(self):
        if not self.last_push_str:
            return True
        sec = int(time() - 1569254400)
        day = sec % (60 * 60 * 24)
        hour = day / (60 * 60)
        if hour > 23 or hour < 9:
            return False
        return True

    @staticmethod
    def __markdown_msg(context=''):
        _time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        _pack = {
            'msgtype': 'markdown',
            'markdown': {'title': _time, 'text': '#### {}\n{}'.format(_time, context)}
        }
        try:
            return json.dumps(_pack)
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None

    def post_msg(self, context=''):
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        data = self.__markdown_msg(context)
        try:
            req = request.Request(self.robot, data=bytes(data, 'utf-8'), headers=headers)
            with closing(request.urlopen(req, timeout=5)) as resp:
                context = resp.read().decode('utf-8')
                context = json.loads(context)
                if context['errcode'] == 0:
                    return True
        except Exception as e:
            if 'timed out' in str(e):
                write_log(str(e))
            else:
                write_log('{}\n{}'.format(e, format_exc()))
        return False

    @staticmethod
    def get_wacai():
        tms = int(time() * 1000)
        url = 'https://www.wacai.com/setting/account_list.action?reqBalance=false?timesamp={}'.format(tms)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': (
                'JSESSIONID=BF4803534D7A5201988FDFE72D6AF42C; '
                'sajssdk_2015_cross_new_user=1; '
                'sensorsdata2015jssdkcross=%7B%22'
                'distinct_id%22%3A%2216d63bfe74b3e1-08e0dcf4673ea8-47754016-1049088-16d63bfe74c47%22%2C%22%24'
                'device_id%22%3A%2216d63bfe74b3e1-08e0dcf4673ea8-47754016-1049088-16d63bfe74c47%22%2C%22'
                'props%22%3A%7B%22%24'
                'latest_referrer%22%3A%22%22%2C%22%24'
                'latest_referrer_host%22%3A%22%22%2C%22%24'
                'latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24'
                'latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_'
                '%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; '
                'wctk=WCeO2k48odHUzPZPYLKsjchOGegdjZkS1KhjA; '
                'wctk.sig=frmbhuZ7tbIc3XY2-gvGsbMuaiU; '
                'access_token=WCeO2k48odHUzPZPYLKsjchOGegdjZkS1KhjA; '
                'access_token.sig=b2DLvmTde4k-f4KW-nGkDhZ7oDQ; '
            ),
            'Host': 'www.wacai.com',
            'Referer': 'https://www.wacai.com/user/user.action',
            'User-Agent': (
                'Mozilla/5.0 '
                '(Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 '
                '(KHTML, like Gecko) '
                'Chrome/70.0.3538.25 '
                'Safari/537.36 Core/1.70.3722.400 '
                'QQBrowser/10.5.3738.400'
            ),
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = {
            'type': 'all',
            'reqBalance': 'true',
            'pageInfo.pageIndex': '1',
            'hidden': 'false'
        }
        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, data, headers)
            with closing(request.urlopen(req, timeout=3)) as resp:
                context = resp.read()
                if resp.info().get('Content-Encoding') == 'gzip':
                    context = gzip.decompress(context).decode('utf-8')
                else:
                    context = context.decode('utf-8')
                resp_dict = json.loads(context)
                value = 0
                disk = 0
                capacity = 0
                cost = 0
                power = 0
                for account in resp_dict['accountTypeSum']:
                    if 'accTypeName' not in account.keys():
                        continue
                    if account['accTypeName'] == '投资账户':
                        for accs in account['accs']:
                            if accs['name'] == '矿工':
                                value = round(accs['balance'], 2)
                                comment = accs['comment'].split('\n')
                                disk = int(comment[0].split('=')[1])
                                capacity = int(comment[1].split('=')[1])
                                cost = float(comment[2].split('=')[1])
                                power = int(comment[3].split('=')[1])
                if (value + disk + capacity + cost + power) != 0:
                    return [value, disk, capacity, cost, power]
        except Exception as e:
            if 'timed out' in str(e):
                write_log(str(e))
            else:
                write_log('{}\n{}'.format(e, format_exc()))
        return None

    def get_trade(self, symbol):
        headers = {
            'User-Agent': self.user_agent
        }
        try:
            if symbol == 'BOOM' or symbol == 'BURST':
                headers['Host'] = 'www.qbtc.ink'
                url = 'http://www.qbtc.ink/json/depthTable.do?tradeMarket=CNYT&symbol={}'.format(symbol)
            elif symbol == 'BHD':
                url = 'https://api.aex.zone/depth.php?c={}&mk_type=cnc'.format(symbol)
            elif symbol == 'HDD':
                url = 'https://openapi.bitmart.io/v2/ticker?symbol={}_BHD'.format(symbol)
            else:   # symbol == 'LHD':
                url = 'https://openapi.bitmart.io/v2/ticker?symbol={}_BHD'.format(symbol)
            req = request.Request(url=url, headers=headers)
            with closing(request.urlopen(req, timeout=10)) as resp:
                context = resp.read().decode('utf-8')
                context = json.loads(context)
                if symbol == 'BOOM' or symbol == 'BURST':
                    data_list = [float(context['result']['buy'][0]['price']), float(context['result']['sell'][0]['price'])]
                elif symbol == 'BHD':
                    data_list = [float(context['bids'][0][0]), float(context['asks'][0][0])]
                elif symbol == 'HDD':
                    data_list = [float(context['bid_1']), float(context['ask_1'])]
                else:   # symbol == 'LHD':
                    data_list = [float(context['bid_1']), float(context['ask_1'])]
                return data_list
        except Exception as e:
            if 'timed out' in str(e):
                write_log('get {} price timed out'.format(symbol))
            else:
                write_log('get {} price\n{}\n{}'.format(symbol, e, format_exc()))
        return None

    def get_property(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': (
                'language=zh-CN; '
                'sd7038915=q9mjqnc651daad8i6gpum1uqf7; '
                'loginName=mark3333520%40163.com; '
                'loginPwd=f3in2oWmp61%2F'
                'dHqnfanUzo6oqWKMjKnOl4h%2B'
                'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
                'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
                'pZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf;'
            ),
            'Host': 'www.onepool.co',
            'Referer': 'http://www.onepool.co/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent
        }
        cur_url = 'http://www.onepool.co/home/user/asset.html'
        try:
            req = request.Request(cur_url, headers=headers)
            with closing(request.urlopen(req, timeout=5)) as resp:
                context = resp.read()
                if resp.info().get('Content-Encoding') == 'gzip':
                    context = gzip.decompress(context).decode('utf-8')
                else:
                    context = context.decode('utf-8')
                html = etree.HTML(context)
                # BHD:['2.13215185']
                # Burst:['285.16030599']
                # Boom:['3.65841511']
                # Boom:['0.00000000']
                # Newbi:['0.00000000']
                # LHD:['0.95614178']
                # LHD:['0.00000000']
                # Disc:['0.00000000']
                # HDD:['0.00000000']
                # BOOM:['377.40413118']
                # LHD:['18.12297426']
                cur_property = {}
                cur_matters = {}
                for tr in html.xpath('//div[@class="layui-tab-content"]/div[1]/div/table/tbody/tr'):
                    coin_name = tr.xpath('td[1]/text()')[1].strip().split(' ')[0].upper()
                    if tr.xpath('td[1]/lan/@t'):
                        if tr.xpath('td[1]/lan/@t')[0] == 'user_asset_mort':
                            continue
                    cur_property[coin_name] = float(tr.xpath('td[4]/text()')[0])
                for tr in html.xpath('//div[@class="layui-tab-content"]/div[2]/div/table/tbody/tr'):
                    coin_name = tr.xpath('td[1]/text()')[1].strip().split(' ')[0].upper()
                    cur_matters[coin_name] = float(tr.xpath('td[2]/text()')[0]) + float(tr.xpath('td[4]/text()')[0])
                if 'BHD' in cur_property.keys() and \
                        'HDD' in cur_property.keys() and \
                        'LHD' in cur_property.keys() and \
                        'BOOM' in cur_property.keys() and \
                        'BURST' in cur_property.keys() and \
                        'BOOM' in cur_matters.keys() and \
                        'LHD' in cur_matters.keys():
                    bhd_property = cur_property['BHD']
                    hdd_property = cur_property['HDD']
                    burst_property = cur_property['BURST']
                    lhd_property = cur_property['LHD'] + cur_matters['LHD']
                    boom_property = cur_property['BOOM'] + cur_matters['BOOM']
                    return [bhd_property, hdd_property, lhd_property, boom_property, burst_property]
        except Exception as e:
            if 'timed out' in str(e):
                write_log(str(e))
            else:
                write_log('{}\n{}'.format(e, format_exc()))
        return None

    def get_profit_date_to_list(self, symbol, t_start, t_stop):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '38',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': (
                'language=zh-CN; '
                'sd7038915=q9mjqnc651daad8i6gpum1uqf7; '
                'loginName=mark3333520%40163.com; '
                'loginPwd=f3in2oWmp61%2F'
                'dHqnfanUzo6oqWKMjKnOl4h%2B'
                'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
                'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
                'pZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf;'
            ),
            'Host': 'www.onepool.co',
            'Origin': 'http://www.onepool.co',
            'Referer': '',
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest'
        }
        if symbol == 'BHD':
            headers['Referer'] = 'http://www.onepool.co/eco-bhd/user/income_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_bhd/user/getincomeinquiry.html'
        elif symbol == 'HDD':
            headers['Referer'] = 'http://www.onepool.co/eco-hdd/user/income_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_hdd/user/getincomeinquiry.html'
        elif symbol == 'LHD':
            headers['Referer'] = 'http://www.onepool.co/eco-lhd/user/income_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_lhd/user/getincomeinquiry.html'
        elif symbol == 'BOOM':
            headers['Referer'] = 'http://www.onepool.co/eco-boom/user/income_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_boom/user/getincomeinquiry.html'
        elif symbol == 'BURST':
            headers['Referer'] = 'http://www.onepool.co/burst/user/income_inquiry.html'
            cur_url = 'http://www.onepool.co/burst/user/getincomeinquiry.html'
        else:
            return None
        try:
            t_start_ts = int(mktime(strptime(t_start, "%Y-%m-%d")))
            t_stop_ts = int(mktime(strptime(t_stop, "%Y-%m-%d")))
            day_list = [strftime("%Y-%m-%d", localtime(x)) for x in range(t_start_ts, t_stop_ts+1, 24*60*60)]
            rt_data = []
            page_idx = 1
            page_total = 1
            while page_idx <= page_total:
                data = {'page': page_idx, 'start': t_start, 'stop': t_stop}
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(cur_url, data=data, headers=headers)
                with closing(request.urlopen(req, timeout=5)) as resp:
                    context = resp.read().decode('utf-8')
                    js_data = json.loads(context)['data']
                    for data in js_data['data']:
                        if data['profit_date'] in day_list:
                            rt_data.append(data)
                    try:
                        page_total = js_data['last_page']
                    except Exception as e:
                        print('{}\n{}'.format(e, format_exc()))
                    page_idx += 1
            return rt_data
        except Exception as e:
            if 'timed out' in str(e):
                write_log('get {} profit list timed out'.format(symbol))
            else:
                write_log('get {} profit list\n{}\n{}'.format(symbol, e, format_exc()))
        return None

    def get_profit_by_date(self, t_start, t_stop='', details=False, bhd=True, hdd=True, lhd=True, boom=True, burst=True):
        if not t_stop:
            t_stop = t_start
        bhd_amount = 0
        if bhd:
            d_list = self.get_profit_date_to_list('BHD', t_start, t_stop)
            if d_list is None:
                return None
            else:
                for data in d_list:
                    bhd_amount += float(data['amount'])
        hdd_amount = 0
        if hdd:
            d_list = self.get_profit_date_to_list('HDD', t_start, t_stop)
            if d_list is None:
                return None
            else:
                for data in d_list:
                    hdd_amount += float(data['amount'])
        lhd_amount = 0
        if lhd:
            d_list = self.get_profit_date_to_list('LHD', t_start, t_stop)
            if d_list is None:
                return None
            else:
                for data in d_list:
                    lhd_amount += float(data['amount'])
        boom_amount = 0
        if boom:
            d_list = self.get_profit_date_to_list('BOOM', t_start, t_stop)
            if d_list is None:
                return None
            else:
                for data in d_list:
                    boom_amount += float(data['amount'])
        burst_amount = 0
        if burst:
            d_list = self.get_profit_date_to_list('BURST', t_start, t_stop)
            if d_list is None:
                return None
            else:
                for data in d_list:
                    burst_amount += float(data['amount'])
        if details:
            if bhd:
                write_log('BHD amount:{}'.format(bhd_amount))
            if hdd:
                write_log('HDD amount:{}'.format(hdd_amount))
            if lhd:
                write_log('LHD amount:{}'.format(lhd_amount))
            if boom:
                write_log('BOOM amount:{}'.format(boom_amount))
            if burst:
                write_log('BURST amount:{}'.format(burst_amount))
        return bhd_amount, hdd_amount, lhd_amount, boom_amount, burst_amount

    def get_theory_date_to_list(self, symbol, t_start, t_stop):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '82',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '',
            'Origin': '',
            'Referer': '',
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': (
                'language=zh-CN; '
                'sd7038915=q9mjqnc651daad8i6gpum1uqf7; '
                'loginName=mark3333520%40163.com; '
                'loginPwd=f3in2oWmp61%2F'
                'dHqnfanUzo6oqWKMjKnOl4h%2B'
                'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
                'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
                'pZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf;'
            )
        }
        if symbol == 'BHD':
            headers['Host'] = 'www.onepool.co'
            headers['Origin'] = 'http://www.onepool.co'
            headers['Referer'] = 'http://www.onepool.co/eco-bhd/user/detail_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_bhd/user/getdetailinquiry.html'
        elif symbol == 'HDD':
            headers['Host'] = 'www.onepool.co'
            headers['Origin'] = 'http://www.onepool.co'
            headers['Referer'] = 'http://www.onepool.co/eco-hdd/user/detail_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_hdd/user/getdetailinquiry.html'
            return []
        elif symbol == 'LHD':
            headers['Host'] = 'www.onepool.co'
            headers['Origin'] = 'http://www.onepool.co'
            headers['Referer'] = 'http://www.onepool.co/eco-lhd/user/detail_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_lhd/user/getdetailinquiry.html'
        elif symbol == 'BOOM':
            headers['Host'] = 'www.onepool.co'
            headers['Origin'] = 'http://www.onepool.co'
            headers['Referer'] = 'http://www.onepool.co/eco-boom/user/detail_inquiry.html'
            cur_url = 'http://www.onepool.co/eco_boom/user/getdetailinquiry.html'
        elif symbol == 'BURST':
            headers['Host'] = 'www.onepool.co'
            headers['Origin'] = 'http://www.onepool.co'
            headers['Referer'] = 'http://www.onepool.co/burst/user/detail_inquiry.html'
            cur_url = 'http://www.onepool.co/burst/user/getdetailinquiry.html'
        else:
            return []
        try:
            rt_data = []
            data = {'page': '1', 'start': t_start, 'end': t_stop, 'is_distribution': '0'}
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(cur_url, data=data, headers=headers)
            with closing(request.urlopen(req, timeout=3)) as resp:
                context = resp.read().decode('utf-8')
                js_data = json.loads(context)['data']
                for data in js_data['data']:
                    rt_data.append(data)
            return rt_data
        except Exception as e:
            if 'timed out' in str(e):
                write_log(str(e))
            else:
                write_log('{}\n{}'.format(e, format_exc()))
        return []

    def get_theory(self, details=False, bhd=True, hdd=True, lhd=True, boom=True, burst=True):
        t_start = strftime("%Y-%m-%d %H:%M:%S", localtime(time() - 3 * 24 * 60 * 60))
        t_stop = strftime("%Y-%m-%d %H:%M:%S", localtime())
        bhd_amount = 0
        if bhd:
            try:
                for data in self.get_theory_date_to_list('BHD', t_start, t_stop):
                    bhd_amount += float(data['amount'])
            except Exception as e:
                write_log('{}\n{}'.format(e, format_exc()))
                return None
        hdd_amount = 0
        if hdd:
            try:
                for data in self.get_theory_date_to_list('HDD', t_start, t_stop):
                    hdd_amount += float(data['amount'])
            except Exception as e:
                write_log('{}\n{}'.format(e, format_exc()))
                return None
        lhd_amount = 0
        if lhd:
            try:
                for data in self.get_theory_date_to_list('LHD', t_start, t_stop):
                    lhd_amount += float(data['amount'])
            except Exception as e:
                write_log('{}\n{}'.format(e, format_exc()))
                return None
        boom_amount = 0
        if boom:
            try:
                for data in self.get_theory_date_to_list('BOOM', t_start, t_stop):
                    boom_amount += float(data['amount'])
            except Exception as e:
                write_log('{}\n{}'.format(e, format_exc()))
                return None
        burst_amount = 0
        if burst:
            try:
                for data in self.get_theory_date_to_list('BURST', t_start, t_stop):
                    burst_amount += float(data['amount'])
            except Exception as e:
                write_log('{}\n{}'.format(e, format_exc()))
                return None
        if details:
            if bhd:
                write_log('BHD amount:{}'.format(bhd_amount))
            if hdd:
                write_log('HDD amount:{}'.format(hdd_amount))
            if boom:
                write_log('BOOM amount:{}'.format(boom_amount))
            if burst:
                write_log('BURST amount:{}'.format(burst_amount))
        return bhd_amount, hdd_amount, lhd_amount, boom_amount, burst_amount

    def on_thread_wacai(self):
        # 线程获取挖财数据，720分钟获取一次，获取失败则5秒后重试
        wacai_ts = time()
        wacai_tout = 0
        while True:
            if not self.__get_valid_time():
                sleep(60)
                continue
            if (time() - wacai_ts) >= wacai_tout:
                wacai_ts = time()
                wacai_tout = 60
                data = self.get_wacai()
                if data:
                    wacai_tout = 60 * 720
                    Machine, Disk, Capacity, Price, Pow = data
                    if Machine > self.cycMachine:
                        self.cycMachine = Machine
                    if Disk > self.cycDisk:
                        self.cycDisk = Disk
                    if Capacity > self.cycCapacity:
                        self.cycCapacity = Capacity
                    if Price > self.cycPrice:
                        self.cycPrice = Price
                    if Pow > self.cycPow:
                        self.cycPow = Pow
                    write_log('获取挖财数据：{}'.format(data))
            sleep(5)

    def on_thread_trade(self):
        # 线程获取实时报价，40分钟获取一次，获取失败则5秒后重试
        trade_bhd_ts = time()
        trade_hdd_ts = time()
        trade_lhd_ts = time()
        trade_boom_ts = time()
        trade_burst_ts = time()
        trade_bhd_tout = 0
        trade_hdd_tout = 0
        trade_lhd_tout = 0
        trade_boom_tout = 0
        trade_burst_tout = 0
        default_tout = 60 * 40
        while True:
            if not self.__get_valid_time():
                sleep(60)
                continue
            if (time() - trade_bhd_ts) >= trade_bhd_tout:
                trade_bhd_ts = time()
                trade_bhd_tout = 60
                price = self.get_trade('BHD')
                if price:
                    trade_bhd_tout = default_tout
                    self.tradeBHD = price
                    write_log('获取BHD价格：{}'.format(price))
            if (time() - trade_hdd_ts) >= trade_hdd_tout:
                trade_hdd_ts = time()
                trade_hdd_tout = 60
                price = self.get_trade('HDD')
                if price:
                    trade_hdd_tout = default_tout
                    self.tradeHDD = price
                    write_log('获取HDD价格：{}'.format(price))
            if (time() - trade_lhd_ts) >= trade_lhd_tout:
                trade_lhd_ts = time()
                trade_lhd_tout = 60
                price = self.get_trade('LHD')
                if price:
                    trade_lhd_tout = default_tout
                    self.tradeLHD = price
                    write_log('获取LHD价格：{}'.format(price))
            if (time() - trade_boom_ts) >= trade_boom_tout:
                trade_boom_ts = time()
                trade_boom_tout = 60
                price = self.get_trade('BOOM')
                if price:
                    trade_boom_tout = default_tout
                    self.tradeBOOM = price
                    write_log('获取BOOM价格：{}'.format(price))
            if (time() - trade_burst_ts) >= trade_burst_tout:
                trade_burst_ts = time()
                trade_burst_tout = 60
                price = self.get_trade('BURST')
                if price:
                    trade_burst_tout = default_tout
                    self.tradeBURST = price
                    write_log('获取BURST价格：{}'.format(price))
            sleep(5)

    def on_thread_average(self):
        # 线程获取日均收益，120分钟获取一次，获取失败则5秒后重试
        # '2019-07-18'  15号盘重新Plot后上线时间
        # '2019-08-07'  16号盘Plot后上线时间
        average_ts = time()
        average_tsout = 0
        average_days = 7
        default_tsout = 60 * 120
        while True:
            if not self.__get_valid_time():
                sleep(60)
                continue
            if (time() - average_ts) >= average_tsout and \
                    self.tradeBHD and \
                    self.tradeHDD and \
                    self.tradeLHD and \
                    self.tradeBOOM and \
                    self.tradeBURST:
                average_ts = time()
                average_tsout = 60
                yesterday = strftime("%Y-%m-%d", localtime(time() - 24 * 60 * 60))
                lastweek = strftime("%Y-%m-%d", localtime(time() - average_days * 24 * 60 * 60))
                data = self.get_profit_by_date(lastweek, yesterday, details=False)
                if data:
                    average_tsout = default_tsout
                    bhd_amount, hdd_amount, lhd_amount, boom_amount, burst_amount = data
                    total_income = bhd_amount * self.tradeBHD[0]
                    total_income += hdd_amount * self.tradeHDD[0]
                    total_income += lhd_amount * self.tradeLHD[0]
                    total_income += boom_amount * self.tradeBOOM[0]
                    total_income += burst_amount * self.tradeBURST[0]
                    self.poolAverage = total_income / average_days
                    write_log('获取矿池日均收益：{}'.format(self.poolAverage))
            sleep(5)

    def on_thread_property(self):
        # 线程获取矿池资产，40分钟获取一次，获取失败则5秒后重试
        property_ts = time()
        property_tout = 0
        default_tout = 60 * 40
        while True:
            if not self.__get_valid_time():
                sleep(60)
                continue
            if (time() - property_ts) >= property_tout:
                property_ts = time()
                property_tout = 60
                data = self.get_property()
                if data:
                    property_tout = default_tout
                    self.bhdAmount, self.hddAmount, self.lhdAmount, self.boomAmount, self.burstAmount = data
                    write_log('获取ONEPOOL资产：{}'.format(data))
            sleep(5)

    def on_thread_today(self):
        # 线程获取当日收益，30分钟获取一次，获取失败则5秒后重试
        today_ts = time()
        future_ts = time()
        today_tout = 0
        future_tout = 0
        default_tout = 60 * 30
        while True:
            if not self.__get_valid_time():
                sleep(60)
                continue
            today = strftime("%Y-%m-%d", localtime())
            if (time() - today_ts) >= today_tout:
                today_ts = time()
                today_tout = 60
                data = self.get_profit_by_date(today)
                if data:
                    self.bhdToday, self.hddToday, self.lhdToday, self.boomToday, self.burstToday = data
                    today_tout = default_tout
                    write_log('获取当日收益：{}'.format(data))
            if (time() - future_ts) >= future_tout:
                future_ts = time()
                future_tout = 60
                data = self.get_theory()
                if data:
                    self.bhdFuture, self.hddFuture, self.lhdFuture, self.boomFuture, self.burstFuture = data
                    future_tout = default_tout
                    write_log('获取未分配收益：{}'.format(data))
            sleep(5)

    def commit_evt(self):
        # 报价
        if not self.tradeBHD or not self.tradeHDD or not self.tradeLHD or not self.tradeBOOM or not self.tradeBURST:
            print('{} 未正常获取'.format('报价'))
            return False
        bhdBid, bhdAsk = self.tradeBHD
        hddBid, hddAsk = self.tradeHDD
        lhdBid, lhdAsk = self.tradeLHD
        boomBid, boomAsk = self.tradeBOOM
        burstBid, burstAsk = self.tradeBURST

        hddBid, hddAsk = hddBid * bhdBid, hddAsk * bhdAsk
        lhdBid, lhdAsk = lhdBid * bhdBid, lhdAsk * bhdAsk
        # ONEPOOL
        if not self.bhdAmount \
                and not self.hddAmount \
                and not self.lhdAmount \
                and not self.boomAmount \
                and not self.burstAmount:
            print('{} 未正常获取'.format('ONEPOOL资产'))
            return False
        bhdProperty = self.bhdAmount * bhdBid
        hddProperty = self.hddAmount * hddBid
        lhdProperty = self.lhdAmount * lhdBid
        boomProperty = self.boomAmount * boomBid
        burstProperty = self.burstAmount * burstBid
        poolProperty = bhdProperty + hddProperty + lhdProperty + boomProperty + burstProperty
        self.bhdDayinc = self.bhdToday * bhdBid
        self.hddDayinc = self.hddToday * hddBid
        self.lhdDayinc = self.lhdToday * lhdBid
        self.boomDayinc = self.boomToday * boomBid
        self.burstDayinc = self.burstToday * burstBid
        poolToday = self.bhdDayinc + self.hddDayinc + self.lhdDayinc + self.boomDayinc + self.burstDayinc
        # 用电统计
        if not self.cycPrice or not self.cycPow:
            print('{} 未正常获取'.format('用电信息'))
            return False
        cycPay = self.cycPow * 24 * 30 * self.cycPrice / 1000
        # 周期
        if not self.cycMachine or not self.cycDisk or not self.cycCapacity:
            print('{} 未正常获取'.format('设备信息'))
            return False
        if not self.poolAverage:
            print('{} 未正常获取'.format('日均收益'))
            return False
        cycIncome = self.poolAverage * 30
        cycProfit = cycIncome - cycPay
        cycMonth = (self.cycMachine - poolProperty) / cycProfit
        cycDate = time() + cycMonth * 30 * 24 * 60 * 60
        if not os.path.isfile(self.template):
            print('{} 未正常获取'.format('Markdown模板'))
            return False
        
        # 判断数据增长或减少
        self.this_push_dict['bhdBid'] = round(bhdBid, 2)
        self.this_push_dict['bhdAsk'] = round(bhdAsk, 2)
        self.this_push_dict['hddBid'] = round(hddBid, 2)
        self.this_push_dict['hddAsk'] = round(hddAsk, 2)
        self.this_push_dict['lhdBid'] = round(lhdBid, 2)
        self.this_push_dict['lhdAsk'] = round(lhdAsk, 2)
        self.this_push_dict['boomBid'] = round(boomBid, 2)
        self.this_push_dict['boomAsk'] = round(boomAsk, 2)
        self.this_push_dict['burstBid'] = round(burstBid, 2)
        self.this_push_dict['burstAsk'] = round(burstAsk, 2)

        self.this_push_dict['poolProperty'] = round(poolProperty, 2)
        self.this_push_dict['poolToday'] = round(poolToday, 2)
        self.this_push_dict['poolAverage'] = round(self.poolAverage, 2)

        self.this_push_dict['bhdToday'] = round(self.bhdToday, 2)
        self.this_push_dict['bhdFuture'] = round(self.bhdFuture, 2)
        self.this_push_dict['bhdDayinc'] = round(self.bhdDayinc, 2)
        self.this_push_dict['bhdAmount'] = round(self.bhdAmount, 2)
        self.this_push_dict['bhdProperty'] = round(bhdProperty, 2)
        self.this_push_dict['hddToday'] = round(self.hddToday, 2)
        self.this_push_dict['hddFuture'] = round(self.hddFuture, 2)
        self.this_push_dict['hddDayinc'] = round(self.hddDayinc, 2)
        self.this_push_dict['hddAmount'] = round(self.hddAmount, 2)
        self.this_push_dict['hddProperty'] = round(hddProperty, 2)
        self.this_push_dict['lhdToday'] = round(self.lhdToday, 2)
        self.this_push_dict['lhdFuture'] = round(self.lhdFuture, 2)
        self.this_push_dict['lhdDayinc'] = round(self.lhdDayinc, 2)
        self.this_push_dict['lhdAmount'] = round(self.lhdAmount, 2)
        self.this_push_dict['lhdProperty'] = round(lhdProperty, 2)
        self.this_push_dict['boomToday'] = round(self.boomToday, 2)
        self.this_push_dict['boomFuture'] = round(self.boomFuture, 2)
        self.this_push_dict['boomDayinc'] = round(self.boomDayinc, 2)
        self.this_push_dict['boomAmount'] = round(self.boomAmount, 2)
        self.this_push_dict['boomProperty'] = round(boomProperty, 2)
        self.this_push_dict['burstToday'] = round(self.burstToday, 2)
        self.this_push_dict['burstFuture'] = round(self.burstFuture, 2)
        self.this_push_dict['burstDayinc'] = round(self.burstDayinc, 2)
        self.this_push_dict['burstAmount'] = round(self.burstAmount, 2)
        self.this_push_dict['burstProperty'] = round(burstProperty, 2)

        self.this_push_dict['cycPrice'] = round(self.cycPrice, 2)
        self.this_push_dict['cycPow'] = round(self.cycPow, 2)
        self.this_push_dict['cycPay'] = round(cycPay, 2)
        self.this_push_dict['cycMachine'] = round(self.cycMachine, 2)
        self.this_push_dict['cycDisk'] = round(self.cycDisk, 2)
        self.this_push_dict['cycCapacity'] = round(self.cycCapacity, 2)
        self.this_push_dict['cycIncome'] = round(cycIncome, 2)
        self.this_push_dict['cycProfit'] = round(cycProfit, 2)
        self.this_push_dict['cycMonth'] = round(cycMonth, 2)
        self.this_push_dict['cycDate'] = int(cycDate)

        change_flag = False
        for key in self.item:
            if key == 'cycDate':
                if int(self.this_push_dict[key]/86400) > int(self.last_push_dict[key]/86400):
                    self.this_push_direct[key] = '↑'
                    change_flag = True
                elif int(self.this_push_dict[key]/86400) < int(self.last_push_dict[key]/86400):
                    self.this_push_direct[key] = '↓'
                    change_flag = True
                else:
                    self.this_push_direct[key] = ''
            else:
                if self.this_push_dict[key] > self.last_push_dict[key]:
                    self.this_push_direct[key] = '↑'
                    change_flag = True
                elif self.this_push_dict[key] < self.last_push_dict[key]:
                    self.this_push_direct[key] = '↓'
                    change_flag = True
                else:
                    self.this_push_direct[key] = ''
        # 写入数据到markdown
        with open(self.template, 'r', encoding='utf-8') as f:
            md = f.read()
        data = md.format(
            bhdBidDirect=self.this_push_direct['bhdBid'], bhdBid=self.this_push_dict['bhdBid'],
            bhdAskDirect=self.this_push_direct['bhdAsk'], bhdAsk=self.this_push_dict['bhdAsk'],
            hddBidDirect=self.this_push_direct['hddBid'], hddBid=self.this_push_dict['hddBid'],
            hddAskDirect=self.this_push_direct['hddAsk'], hddAsk=self.this_push_dict['hddAsk'],
            lhdBidDirect=self.this_push_direct['lhdBid'], lhdBid=self.this_push_dict['lhdBid'],
            lhdAskDirect=self.this_push_direct['lhdAsk'], lhdAsk=self.this_push_dict['lhdAsk'],
            boomBidDirect=self.this_push_direct['boomBid'], boomBid=self.this_push_dict['boomBid'],
            boomAskDirect=self.this_push_direct['boomAsk'], boomAsk=self.this_push_dict['boomAsk'],
            burstBidDirect=self.this_push_direct['burstBid'], burstBid=self.this_push_dict['burstBid'],
            burstAskDirect=self.this_push_direct['burstAsk'], burstAsk=self.this_push_dict['burstAsk'],

            poolPropertyDirect=self.this_push_direct['poolProperty'], poolProperty=self.this_push_dict['poolProperty'],
            poolTodayDirect=self.this_push_direct['poolToday'], poolToday=self.this_push_dict['poolToday'],
            poolAverageDirect=self.this_push_direct['poolAverage'], poolAverage=self.this_push_dict['poolAverage'],

            bhdTodayDirect=self.this_push_direct['bhdToday'], bhdToday=self.this_push_dict['bhdToday'],
            bhdFutureDirect=self.this_push_direct['bhdFuture'], bhdFuture=self.this_push_dict['bhdFuture'],
            bhdDayincDirect=self.this_push_direct['bhdDayinc'], bhdDayinc=self.this_push_dict['bhdDayinc'],
            bhdAmountDirect=self.this_push_direct['bhdAmount'], bhdAmount=self.this_push_dict['bhdAmount'],
            bhdPropertyDirect=self.this_push_direct['bhdProperty'], bhdProperty=self.this_push_dict['bhdProperty'],
            hddTodayDirect=self.this_push_direct['hddToday'], hddToday=self.this_push_dict['hddToday'],
            hddFutureDirect=self.this_push_direct['hddFuture'], hddFuture=self.this_push_dict['hddFuture'],
            hddDayincDirect=self.this_push_direct['hddDayinc'], hddDayinc=self.this_push_dict['hddDayinc'],
            hddAmountDirect=self.this_push_direct['hddAmount'], hddAmount=self.this_push_dict['hddAmount'],
            hddPropertyDirect=self.this_push_direct['hddProperty'], hddProperty=self.this_push_dict['hddProperty'],
            lhdTodayDirect=self.this_push_direct['lhdToday'], lhdToday=self.this_push_dict['lhdToday'],
            lhdFutureDirect=self.this_push_direct['lhdFuture'], lhdFuture=self.this_push_dict['lhdFuture'],
            lhdDayincDirect=self.this_push_direct['lhdDayinc'], lhdDayinc=self.this_push_dict['lhdDayinc'],
            lhdAmountDirect=self.this_push_direct['lhdAmount'], lhdAmount=self.this_push_dict['lhdAmount'],
            lhdPropertyDirect=self.this_push_direct['lhdProperty'], lhdProperty=self.this_push_dict['lhdProperty'],
            boomTodayDirect=self.this_push_direct['boomToday'], boomToday=self.this_push_dict['boomToday'],
            boomFutureDirect=self.this_push_direct['boomFuture'], boomFuture=self.this_push_dict['boomFuture'],
            boomDayincDirect=self.this_push_direct['boomDayinc'], boomDayinc=self.this_push_dict['boomDayinc'],
            boomAmountDirect=self.this_push_direct['boomAmount'], boomAmount=self.this_push_dict['boomAmount'],
            boomPropertyDirect=self.this_push_direct['boomProperty'], boomProperty=self.this_push_dict['boomProperty'],
            burstTodayDirect=self.this_push_direct['burstToday'], burstToday=self.this_push_dict['burstToday'],
            burstFutureDirect=self.this_push_direct['burstFuture'], burstFuture=self.this_push_dict['burstFuture'],
            burstDayincDirect=self.this_push_direct['burstDayinc'], burstDayinc=self.this_push_dict['burstDayinc'],
            burstAmountDirect=self.this_push_direct['burstAmount'], burstAmount=self.this_push_dict['burstAmount'],
            burstPropertyDirect=self.this_push_direct['burstProperty'],
            burstProperty=self.this_push_dict['burstProperty'],

            cycPriceDirect=self.this_push_direct['cycPrice'], cycPrice=self.this_push_dict['cycPrice'],
            cycPowDirect=self.this_push_direct['cycPow'], cycPow=self.this_push_dict['cycPow'],
            cycPayDirect=self.this_push_direct['cycPay'], cycPay=self.this_push_dict['cycPay'],
            cycMachineDirect=self.this_push_direct['cycMachine'], cycMachine=self.this_push_dict['cycMachine'],
            cycDiskDirect=self.this_push_direct['cycDisk'], cycDisk=self.this_push_dict['cycDisk'],
            cycCapacityDirect=self.this_push_direct['cycCapacity'], cycCapacity=self.this_push_dict['cycCapacity'],
            cycIncomeDirect=self.this_push_direct['cycIncome'], cycIncome=self.this_push_dict['cycIncome'],
            cycProfitDirect=self.this_push_direct['cycProfit'], cycProfit=self.this_push_dict['cycProfit'],
            cycMonthDirect=self.this_push_direct['cycMonth'], cycMonth=self.this_push_dict['cycMonth'],
            cycDateDirect=self.this_push_direct['cycDate'],
            cycDate=strftime('%Y-%m-%d', localtime(self.this_push_dict['cycDate']))
        )
        # 判断数据是否上报过
        if data == self.last_push_str or not change_flag:
            return False
        if (time() - self.robot_ts) >= self.robot_tout:
            if self.post_msg(data):
                self.robot_ts = time()
                self.last_push_str = data
                # for key in self.item:
                #     if self.this_push_direct[key]:
                #         print('{} change to {}'.format(key, self.this_push_dict[key]))
                for key in self.item:
                    self.last_push_dict[key] = self.this_push_dict[key]
                write_log('上报新数据')

    def run(self):
        # Thread get self.cycMachine, self.cycDisk, self.cycCapacity
        # Thread get self.tradeBHD, self.tradeBOOM, self.tradeBURST
        # Thread get self.bhdAmount, self.boomAmount, self.burstAmount
        while True:
            if not self.__get_valid_time():
                sleep(60)
                continue
            self.commit_evt()
            sleep(10)


if __name__ == '__main__':
    app = Pool()
    # app = Pool(True)
    # print(app.get_wacai())
