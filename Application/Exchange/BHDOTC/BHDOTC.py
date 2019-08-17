#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib import request

import logging
import traceback
from md_logging import setup_log

setup_log()
write_log = logging.getLogger('BHDOTC')


class BhdOtc(object):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 6.1; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/70.0.3538.25 '
            'Safari/537.36 Core/1.70.3719.400 '
            'QQBrowser/10.5.3715.400'
        )
    }
    url = 'https://www.bhdotc.io/api/otc/otc?page=1&size=10&tradeType=%s&coin=bhd&symbol=cny'

    def __init__(self):
        pass

    def get_market(self, direction='s'):
        # s:卖家 b:买家
        try:
            req = request.Request(self.url % direction, headers=self.headers)
            resp = request.urlopen(req).read().decode('utf-8')
            data = json.loads(resp)
            info_list = []
            for row in data['rows']:
                print('{}：{} 数量：{} 单价：{} 最低限额：{}{}'.format(
                    ('卖家' if direction == 's' else '买家'),
                    row['userInfo']['nickname'],
                    row['amount'],
                    row['price'],
                    row['minQuantity'],
                    ('BHD' if direction == 's' else 'CNY')
                ))
                row_dict = {
                    'direction': direction,
                    'name': row['userInfo']['nickname'],
                    'amount': row['amount'],
                    'price': row['price'],
                    'minQuantity': row['minQuantity']
                }
                info_list.append(row_dict)
            return info_list
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return None


if __name__ == '__main__':
    otc = BhdOtc()
    otc.get_market('s')
    otc.get_market('b')
