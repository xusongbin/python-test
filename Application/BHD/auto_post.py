#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    def __init__(self):
        self.uupool = UUPool()
        self.onepool = ONEPool()
        self.cointrade = CoinTrade()
        self.dingpost = DingPost()

        self.update_list = []
        self.update_ts = 0
        self.update_flag = True
        self.pow_price = 1.3
        self.pow_power = 210
        self.pow_today = self.pow_power * 24 * 1.3 / 1000
        self.pow_month = self.pow_today * 30
        self.spend = 23200

        self.run()

    def check_post_able(self):
        if not self.update_flag:
            return False
        if (time() - self.update_ts) < 4 * 3600 and self.update_ts != 0:
            return False
        if (time() % (24 * 3600)) < 8 * 3600:       # AM:08:00
            return False
        self.update_flag = False
        self.update_ts = time()
        return True

    def run(self):
        while True:
            sleep(5)
            coin_trade = self.cointrade.get_trade()
            if not coin_trade['valid']:
                continue
            onepool_property = self.onepool.get_property()
            if not onepool_property['valid']:
                continue
            uupool_property = self.uupool.get_property()
            if not uupool_property['valid']:
                continue
            bhd_today_value = uupool_property['BHD']['today'] * coin_trade['BHD']['bid']
            lhd_today_value = uupool_property['LHD']['today'] * coin_trade['LHD']['bid']
            boom_today_value = onepool_property['BOOM']['today'] * coin_trade['BOOM']['bid']
            burst_today_value = onepool_property['BURST']['today'] * coin_trade['BURST']['bid']
            bhd_average_value = uupool_property['BHD']['average'] * coin_trade['BHD']['bid']
            lhd_average_value = uupool_property['LHD']['average'] * coin_trade['LHD']['bid']
            boom_average_value = onepool_property['BOOM']['average'] * coin_trade['BOOM']['bid']
            burst_average_value = onepool_property['BURST']['average'] * coin_trade['BURST']['bid']
            bhd_assert_value = uupool_property['BHD']['amount'] * coin_trade['BHD']['bid']
            lhd_assert_value = uupool_property['LHD']['amount'] * coin_trade['LHD']['bid']
            boom_assert_value = onepool_property['BOOM']['amount'] * coin_trade['BOOM']['bid']
            burst_assert_value = onepool_property['BURST']['amount'] * coin_trade['BURST']['bid']
            coin_total_assert = bhd_assert_value + lhd_assert_value + boom_assert_value + burst_assert_value
            coin_average_value = bhd_average_value + lhd_average_value + boom_average_value + burst_average_value
            coin_month_value = coin_average_value * 30
            coin_today_value = bhd_today_value + lhd_today_value + boom_today_value + burst_today_value
            coin_average_profit = coin_average_value - self.pow_today
            coin_month_profit = coin_month_value - self.pow_month
            coin_cycle_days = int(self.spend / coin_average_profit)
            coin_cycle_date = strftime("%Y-%m-%d", localtime(time() + coin_cycle_days * 24 * 3600))
            _update_list = [
                coin_trade['BHD']['bid'], coin_trade['BHD']['ask'],
                uupool_property['BHD']['today'], bhd_today_value,
                uupool_property['BHD']['average'], bhd_average_value,

                coin_trade['LHD']['bid'], coin_trade['LHD']['ask'],
                uupool_property['LHD']['today'], lhd_today_value,
                uupool_property['LHD']['average'], lhd_average_value,

                coin_trade['BOOM']['bid'], coin_trade['BOOM']['ask'],
                onepool_property['BOOM']['today'], boom_today_value,
                onepool_property['BOOM']['average'], boom_average_value,

                coin_trade['BURST']['bid'], coin_trade['BURST']['ask'],
                onepool_property['BURST']['today'], burst_today_value,
                onepool_property['BURST']['average'], burst_average_value,

                coin_total_assert,
                self.pow_month,

                coin_average_value,
                coin_today_value,

                coin_month_value,
                coin_month_profit,

                coin_cycle_date,
                coin_cycle_days
            ]
            if self.update_list != _update_list:
                self.update_list = _update_list
                self.update_flag = True
            if self.check_post_able():
                self.dingpost.post_md_list(_update_list)
                write_log('上报最新数据')


if __name__ == '__main__':
    app = Pool()
