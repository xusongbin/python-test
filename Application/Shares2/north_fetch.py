#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from save_data import Data
from my_driver import *

import gc
gc.set_threshold(50, 10, 10)
gc.enable()


class North(object):
    __url = 'http://data.10jqka.com.cn/hsgt/timedia/type/north/'
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    }

    def __init__(self):
        self.data = Data()

    def get(self):
        try:
            req = requests.get(self.__url, headers=self.__headers, timeout=3)
            content = json.loads(req.content)
            return content
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
        return None

    def fetch(self):
        _ret = self.get()
        if not _ret:
            return False
        try:
            _status_code = _ret['status_code']
            status_msg = _ret['status_msg']
            _day = _ret['data']['update']
            _date = _ret['data']['date']
            _hgt_list = _ret['data']['h']
            _sgt_list = _ret['data']['s']
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))
            return False
        if _status_code != 0:
            write_log('North status error {}'.format(_status_code))
            return False
        if status_msg.lower() != 'ok':
            write_log('North msg error {}'.format(status_msg))
            return False
        _day_list = ['{} {}:{}:00'.format(_day, x[0:2], x[2:]) for x in _date]
        _total_list = [round(_hgt_list[x] + _sgt_list[x], 2) for x in range(len(_hgt_list))]
        _ndata = np.array([_day_list, _hgt_list, _sgt_list, _total_list]).T
        return _ndata


def main():
    north = North()
    print(north.fetch())


if __name__ == '__main__':
    main()
