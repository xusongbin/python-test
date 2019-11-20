#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import time
from requests import get

database_result_item = \
    ('hash,height,time,difficulty,capacity,baseTarget,plotterId,nonce,deadline,txCount,generator,'
     'address,link,title,'
     'previousblockhash,nextblockhash')

URL = 'https://btchd.org/explorer/api/v2/blockchain/block?page=%d&count=20'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400',
    'Host': 'btchd.org',
    'Referer': 'https://btchd.org/explorer/block',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page=0):
    context = None
    try:
        cur_url = URL % page
        resp = get(cur_url, headers=headers)
        context = resp.text
    except:
        pass
    if not context:
        return None
    page = json.loads(context)
    return page['data']


def get_page_list(page):
    page_list = []
    for i in range(20):
        data = page[i]
        cur_list = []
        for item in database_result_item.split(','):
            try:
                cur_list.append(data[item])
            except:
                cur_list.append('')
        page_list.append(cur_list)
    return page_list


def get_data(start, stop):
    page_list = []
    for num in range(1000):
        page = get_page(num)
        if not page:
            print('get page %d data failure.' % num)
            continue
        print('get page %d data successful.' % num)
        for i in range(20):
            data = page[i]
            if data['time'] > start:
                continue
            if data['time'] < stop:
                return page_list
            cur_list = []
            for item in database_result_item.split(','):
                try:
                    cur_list.append(data[item])
                except:
                    cur_list.append('')
            page_list.append(cur_list)
    return page_list


def parse_data(data):
    name_dict = {
        '3JLVceFYAgWsq8jk97w7FA1itvGvg7WKBn': 'HPool',
        '38JTS1KcD1ajsvA6aL7g7XYexaKZt4WiEe': 'HPool ECO',
        '33NZ7dPrUZALy2LkRjQEe1WhMKGZyTaHtc': 'HDPool',
        '363iEUsQFzcWuwoajSQwz7YZkxTfbqhwkB': 'HDPool ECO',
        '3HHo4j1dbpWrX2YvQjsjNAZqbpXThKvXWW': 'ONEPool ECO',
        '37ahFaegsA5662VVCt4dgy2fS1Rz8w9Csg': 'AWPool'
    }
    count = {}
    addr = {}
    for dat in data:
        # print(dat[1] + ' ' + dat[10] + ' ' + dat[13])
        if dat[13]:
            if dat[13] not in count.keys():
                count[dat[13]] = 1
            else:
                count[dat[13]] += 1
        else:
            if 'other' not in count.keys():
                count['other'] = 1
            else:
                count['other'] += 1
        if dat[10] not in addr.keys():
            addr[dat[10]] = 1
        else:
            addr[dat[10]] += 1
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_count)
    sorted_addr = sorted(addr.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_addr)
    for addr, num in sorted_addr:
        name = ''
        if addr in name_dict.keys():
            name = name_dict[addr]
        print('地址：{} 爆块数量：{:<4d} 矿池名称：{}'.format(addr, num, name))


def main():
    start = int(time())
    stop = int(time() - 24 * 60 * 60)
    data = get_data(start, stop)
    # print(data)
    parse_data(data)


if __name__ == '__main__':
    main()
