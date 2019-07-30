#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import gzip
from urllib import request
from urllib import parse
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
    sales_profit = 572 + 216
    wallet_bhd = 1          # wallet + hdpool + bitatm
    wallet_boom = 0         # wallet
    wallet_burst = 0        # wallet

    def __init__(self):
        self.price_bhd = self.get_price('BHD')
        self.price_boom = self.get_price('BOOM')
        self.price_burst = self.get_price('BURST')
        write_log('BHD price:{}'.format(self.price_bhd))
        write_log('BOOM price:{}'.format(self.price_boom))
        write_log('BURST price:{}'.format(self.price_burst))
        write_log('')

        self.property_bhd = self.get_onepool('BHD')
        self.property_boom = self.get_onepool('BOOM')
        self.property_burst = self.get_onepool('BURST')
        property_all = self.property_bhd * self.price_bhd
        property_all += self.property_boom * self.price_boom
        property_all += self.property_burst * self.price_burst
        write_log('BHD property:{}'.format(self.property_bhd))
        write_log('BOOM property:{}'.format(self.property_boom))
        write_log('BURST property:{}'.format(self.property_burst))
        write_log('TOTAL property:{}'.format(property_all))

        today = strftime("%Y-%m-%d", localtime())
        yesterday = strftime("%Y-%m-%d", localtime(time()-24*60*60))
        # today = '2019-07-29'
        self.day_income(today, details=True)
        num, rate = self.day_income('2019-07-18', yesterday, details=False)
        write_log('')
        self.back_cycle(rate/num)
        write_log('')

    def get_price(self, symbol):
        headers = {
            'User-Agent': self.user_agent
        }
        if symbol == 'BOOM' or symbol == 'BURST':
            headers['Host'] = 'www.qbtc.ink'
            url = 'http://www.qbtc.ink/json/depthTable.do?tradeMarket=CNYT&symbol={}'.format(symbol)
            qbct = True
        else:
            url = 'https://api.aex.zone/depth.php?c={}&mk_type=cnc'.format(symbol)
            qbct = False
        try:
            req = request.Request(url=url, headers=headers)
            resp = request.urlopen(req, timeout=5)
            data = json.loads(resp.read().decode('utf-8'))
            if qbct:
                data = float(data['result']['buy'][0]['price'])
            else:
                data = float(data['bids'][0][0])
            return data
        except Exception as e:
            write_log('get_price except: %s' % e)
        return 0

    def get_onepool(self, symbol):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': (
                'loginName=mark3333520%40163.com; '
                'loginPwd=f3in2oWmp61%2F'
                'dHqnfanUzo6oqWKMjKnOl4h%2B'
                'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
                'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
                'pZySgXu3mJHPrKN%2'
                'FqoJkic6rz47LvZ98o2Wf; '
                'language=zh-CN;'
            ),
            'User-Agent': self.user_agent,
            'Upgrade-Insecure-Requests': '1'
        }
        if symbol == 'BHD':
            headers['Host'] = 'onepool.cc'
            headers['Referer'] = 'http://onepool.cc/eco-bhd/user/income_inquiry.html'
            cur_url = 'http://www.onepool.cc/eco-bhd/user/asset.html'
        elif symbol == 'BOOM':
            headers['Host'] = 'www.onepool.cc'
            headers['Referer'] = 'http://www.onepool.cc/eco-boom/user/income_inquiry.html'
            cur_url = 'http://www.onepool.cc/eco-boom/user/asset.html'
        elif symbol == 'BURST':
            headers['Host'] = 'www.onepool.cc'
            headers['Referer'] = 'http://www.onepool.cc/burst/user/income_inquiry.html'
            cur_url = 'http://www.onepool.cc/burst/user/asset.html'
        else:
            return 0
        try:
            req = request.Request(cur_url, headers=headers)
            resp = request.urlopen(req)
            if resp.info().get('Content-Encoding') == 'gzip':
                resp = gzip.decompress(resp.read()).decode('utf-8')
            else:
                resp = resp.read().decode('utf-8')
            if 'user_asset_avai_balance' not in resp:
                print('Not found property')
                return 0
            resp = resp[:resp.find('user_asset_avai_balance')]
            resp = resp[resp.rfind('asset-num'):]
            data = 0
            for d in re.findall(r'asset-num\">(\d+\.\d+)<.*', resp):
                data = d
            return float(data)
        except Exception as e:
            write_log('get_onepool except: %s' % e)
        return 0

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
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': (
                'loginName=mark3333520%40163.com; '
                'loginPwd=f3in2oWmp61%2F'
                'dHqnfanUzo6oqWKMjKnOl4h%2B'
                'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
                'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
                'pZySgXu3mJHPrKN%2'
                'FqoJkic6rz47LvZ98o2Wf; '
                'language=zh-CN;'
            )
        }
        if symbol == 'BHD':
            headers['Host'] = 'onepool.cc'
            headers['Origin'] = 'http://onepool.cc'
            headers['Referer'] = 'http://onepool.cc/eco-bhd/user/income_inquiry.html'
            cur_url = 'http://onepool.cc/eco_bhd/user/getincomeinquiry.html'
        elif symbol == 'BOOM':
            headers['Host'] = 'www.onepool.cc'
            headers['Origin'] = 'http://www.onepool.cc'
            headers['Referer'] = 'http://www.onepool.cc/eco-boom/user/income_inquiry.html'
            cur_url = 'http://www.onepool.cc/eco_boom/user/getincomeinquiry.html'
        elif symbol == 'BURST':
            headers['Host'] = 'www.onepool.cc'
            headers['Origin'] = 'http://www.onepool.cc'
            headers['Referer'] = 'http://www.onepool.cc/burst/user/income_inquiry.html'
            cur_url = 'http://www.onepool.cc/burst/user/getincomeinquiry.html'
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
                data = parse.urlencode(data).encode('utf-8')
                req = request.Request(cur_url, data=data, headers=headers)
                resp = request.urlopen(req).read().decode('utf-8')
                js_data = json.loads(resp)['data']
                for data in js_data['data']:
                    if data['profit_date'] in day_list:
                        rt_data.append(data)
                try:
                    page_total = js_data['last_page']
                except:
                    pass
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
        local_profit = (self.wallet_bhd + self.property_bhd) * self.price_bhd
        local_profit += (self.wallet_boom + self.property_boom) * self.price_boom
        local_profit += (self.wallet_burst + self.property_burst) * self.price_burst
        write_log('Local profit:{}'.format(local_profit))
        write_log('Sales profit:{}'.format(self.sales_profit))
        month_pay = self.power_waste * self.power_rate * 24 * 30 / 1000
        write_log('Month pay:{}'.format(month_pay))
        month_income = day_income * 30
        write_log('Month income:{}'.format(month_income))
        month_profit = month_income - month_pay
        write_log('Month profit:{}'.format(month_profit))
        month_cycle = (self.machine_price - local_profit - self.sales_profit) / month_profit
        write_log('Month bcycle:{:.1f}'.format(month_cycle))
        target_date = time() + month_cycle * 30 * 24 * 60 * 60
        target_date = strftime('%Y-%m-%d', localtime(target_date))
        write_log('Target date:{}'.format(target_date))


if __name__ == '__main__':
    app = Pool()
