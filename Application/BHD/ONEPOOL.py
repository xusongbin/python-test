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
    power_rate = 1.5
    power_waste = 150
    machine_price = 25000
    wallet_bhd = 0.58527846 + 2.71179041 + 1.50780000 + 0.34834086     # wallet + hdpool + onepool + bitatm
    wallet_boom = 56.66628199 + 13.67252244     # wallet + onepool
    wallet_burst = 25.20733461 + 496.92741351   # wallet + onepool

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

        today = strftime("%Y-%m-%d", localtime())
        self.day_income(today, boom=False)
        num, rate = self.day_income('2019-07-18', today)
        self.back_cycle(rate/num)

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
            day_list = [strftime("%Y-%m-%d", localtime(x)) for x in range(t_start_ts, t_stop_ts+1, 24*60*60)]
            rt_data = []
            page_idx = 1
            page_total = 1
            while page_idx <= page_total:
                data = {'page': page_idx, 'start': t_start, 'stop': t_stop}
                session = requests.session()
                req = session.post(cur_url, data=data, headers=headers, cookies=cookies)
                js_data = json.loads(req.text)['data']
                for data in js_data['data']:
                    if data['profit_date'] in day_list:
                        rt_data.append(data)
                page_total = js_data['last_page']
                page_idx += 1
            return rt_data
        except Exception as e:
            write_log('post_onepool except: %s' % e)
        return []

    def day_income(self, t_start, t_stop='', details=False, bhd=True, boom=True, burst=True):
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
        return day_count, income

    def day_profit(self, day_income):
        power_pay = self.power_waste * self.power_rate * 24 / 1000
        return day_income - power_pay

    def month_profit(self, day_income):
        return self.day_profit(day_income) * 30

    def back_cycle(self, day_income):
        local_profit = self.wallet_bhd * self.price_bhd
        local_profit += self.wallet_boom * self.price_boom
        local_profit += self.wallet_burst * self.price_burst
        write_log('Local profit:{}'.format(local_profit))
        month_pay = self.power_waste * self.power_rate * 24 * 30 / 1000
        write_log('Month pay:{}'.format(month_pay))
        month_income = day_income * 30
        write_log('Month income:{}'.format(month_income))
        month_profit = month_income - month_pay
        write_log('Month profit:{}'.format(month_profit))
        month_cycle = (self.machine_price - local_profit) / month_profit
        write_log('Month bcycle:{:.1f}'.format(month_cycle))


if __name__ == '__main__':
    app = Pool()
