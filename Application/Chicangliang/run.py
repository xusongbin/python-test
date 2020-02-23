#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import requests

headers = {
    'Host': 'data.futures.hexun.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
}

def get_IC2003(date='2020-02-21'):
    url = 'http://data.futures.hexun.com/cccj.aspx?sContract=IC2003&sDate={}&sRank=10'.format(date)
    try:
        resp = requests.get(url, headers=headers, timeout=3)
        print(resp.text)
    except:
        pass


def change_excel():
    ex_name = '持仓量.xlsx'
    ot_name = '持仓量1.xlsx'
    ex_df = pd.read_excel(ex_name)
    ex_list = ex_df.values.tolist()
    print(ex_list)
    resp_name = []
    resp_data = []
    for row in ex_list:
        resp_name.append(row[1])
    for name in resp_name:
        data = 0
        for row in ex_list:
            if row[1] == name:
                data += int(row[2])
            if row[4] == name:
                data += int(row[5])
        resp_data.append(data)
    resp = {}
    for idx, name in enumerate(resp_name):
        resp[name] = resp_data[idx]
    # print(resp)
    resp = sorted(resp.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(resp)
    for idx, row in enumerate(ex_list):
        ex_list[idx].append(idx+1)
        ex_list[idx].append(resp[idx][0])
        ex_list[idx].append(resp[idx][1])
    print(ex_list)
    dd = pd.DataFrame(ex_list)
    print(dd)
    dd.to_excel(ot_name, index=None)


if __name__ == '__main__':
    change_excel()
