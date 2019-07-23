#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
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


class Pool(object):
    user_agent = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
    )

    def __init__(self):
        self.bhd_url = 'http://onepool.cc/eco_bhd/user/getincomeinquiry.html'
        self.burst_url = 'http://www.onepool.cc/burst/user/getincomeinquiry.html'
        self.boom_url = 'http://www.onepool.cc/eco_boom/user/getincomeinquiry.html'

        self.price_bhd = self.get_price('BHD')
        self.price_boom = self.get_price('BOOM')
        self.price_burst = self.get_price('BURST')
        write_log('BHD price:{}'.format(self.price_bhd))
        write_log('BOOM price:{}'.format(self.price_boom))
        write_log('BURST price:{}'.format(self.price_burst))

        self.date_income('2019-07-23', details=True)
        self.date_income('2019-07-18', '2019-07-23', details=True)

    def get_price(self, symbol):
        headers = {
            'User-Agent': self.user_agent
        }
        if symbol == 'BOOM' or symbol == 'BURST':
            headers['Host'] = 'www.qbtc.ink'
            url = 'https://www.qbtc.ink/json/topQuotations.do?tradeMarket=CNYT&symbol={}'.format(symbol)
            qbct = True
        else:
            url = 'https://api.aex.zone/ticker.php?c={}&mk_type=cnc'.format(symbol)
            qbct = False
        try:
            rep = requests.get(url, headers=headers)
            data = json.loads(rep.text)
            if qbct:
                data = float(data['result']['last'])
            else:
                data = float(data['ticker']['last'])
            return data
        except Exception as e:
            write_log('get_burst_price except: %s' % e)
        return None

    def post_onepool(self, symbol, t_start, t_stop):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '38',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '',
            'Origin': '',
            'Referer': '',
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest'
        }
        cookies = {
            'loginName': 'mark3333520%40163.com',
            'loginPwd': (
                'f3in2oWmp61%2FdHqnfanUzo6oqWKMjKnOl4h%2BmK7LlNyMi6zN'
                'hsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2FPv7WVzYyhq9qGtrtoiq'
                'qSp324q86BqLmega97zoBne8u%2FpZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf'
            )
        }
        if symbol == 'BHD':
            headers['Host'] = 'onepool.cc'
            headers['Origin'] = 'http://onepool.cc'
            headers['Referer'] = 'http://onepool.cc/eco-bhd/user/income_inquiry.html'
            cur_url = self.bhd_url
        elif symbol == 'BOOM':
            headers['Host'] = 'www.onepool.cc'
            headers['Origin'] = 'http://www.onepool.cc'
            headers['Referer'] = 'http://www.onepool.cc/eco-boom/user/income_inquiry.html'
            cur_url = self.boom_url
        elif symbol == 'BURST':
            headers['Host'] = 'www.onepool.cc'
            headers['Origin'] = 'http://www.onepool.cc'
            headers['Referer'] = 'http://www.onepool.cc/burst/user/income_inquiry.html'
            cur_url = self.burst_url
        else:
            return []
        try:
            t_start_ts = int(mktime(strptime(t_start, "%Y-%m-%d")))
            t_stop_ts = int(mktime(strptime(t_stop, "%Y-%m-%d")))
            rt_data = []
            for ts in range(t_start_ts, t_stop_ts+1, 24*60*60):
                c_time = strftime("%Y-%m-%d", localtime(ts))
                data = {'page': 1, 'start': c_time, 'stop': c_time}
                session = requests.session()
                req = session.post(cur_url, data=data, headers=headers, cookies=cookies)
                js_data = json.loads(req.text)
                js_data = js_data['data']['data']     # list
                for data in js_data:
                    if data['profit_date'] == c_time:
                        rt_data.append(data)
            return rt_data
        except Exception as e:
            write_log('post_bhd except: %s' % e)
        return []

    def date_income(self, t_start, t_stop='', details=False, bhd=True, boom=True, burst=True):
        if not t_stop:
            t_stop = t_start
        bhd_amount = 0
        if bhd:
            try:
                for data in self.post_onepool('BHD', t_start, t_stop):
                    bhd_amount += float(data['amount'])
            except Exception as e:
                write_log('bhd_amount except: %s' % e)
        boom_amount = 0
        if boom:
            try:
                for data in self.post_onepool('BOOM', t_start, t_stop):
                    boom_amount += float(data['amount'])
            except Exception as e:
                write_log('boom_amount except: %s' % e)
        burst_amount = 0
        if burst:
            try:
                for data in self.post_onepool('BURST', t_start, t_stop):
                    burst_amount += float(data['amount'])
            except Exception as e:
                write_log('burst_amount except: %s' % e)
        if details:
            if bhd:
                write_log('BHD amount:{}'.format(bhd_amount))
            if boom:
                write_log('BOOM amount:{}'.format(boom_amount))
            if burst:
                write_log('BURST amount:{}'.format(burst_amount))
        income = 0
        try:
            income += bhd_amount * self.price_bhd
            income += boom_amount * self.price_boom
            income += burst_amount * self.price_burst
        except Exception as e:
            write_log('income except: %s' % e)
        t_start_ts = int(mktime(strptime(t_start, "%Y-%m-%d")))
        t_stop_ts = int(mktime(strptime(t_stop, "%Y-%m-%d")))
        day_count = int((t_stop_ts - t_start_ts) / (24*60*60)) + 1
        write_log('Time:{}~{} Days:{} Income:{} Average:{}'.format(t_start, t_stop, day_count, income, income/day_count))
        return income


if __name__ == '__main__':
    app = Pool()
