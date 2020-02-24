#!/usr/bin/env python
# -*- coding: utf-8 -*-

import baostock as bs


if __name__ == '__main__':
    lg = bs.login()
    rs = bs.query_history_k_data_plus(
        'sh.000001',
        "date,code,open,high,low,close,preclose,volume,amount",
        '2020-02-24',
        '2020-02-24',
        'd'
    )
    print(rs.get_data())
    bs.logout()
