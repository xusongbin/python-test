#!/usr/bin/env python
# -*- coding: utf-8 -*-

import baostock as bs


def get_day():
    lg = bs.login()
    rs = bs.query_history_k_data(
        'sh.000001',
        "date,code,open,high,low,close,preclose,volume,amount",
        '2020-02-24',
        '2020-02-24',
        'd'
    )
    print(rs.get_data())
    bs.logout()


def get_real():
    bs.login()
    rs = bs.login_real_time(user_id='anonymous', password='123456')
    bs.logout()


if __name__ == '__main__':
    get_real()
