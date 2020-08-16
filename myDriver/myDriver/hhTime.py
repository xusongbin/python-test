#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from time import *


class Time(object):
    @staticmethod
    def now(data=None, rules=None):
        if rules:
            rules = str(rules).upper()
        if type(data) is str:
            data = str(data).replace('/', '-').strip()
            if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', data):
                _ts = strptime(data, '%Y-%m-%d %H:%M:%S')
                _ts = int(mktime(_ts))
            elif re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$', data):
                _tms = data.split('.')[1]
                if len(_tms) > 3:
                    _tms = _tms[:4]
                _tms = int(_tms) / 1000
                _ts = data.split('.')[0]
                _ts = strptime(_ts, '%Y-%m-%d %H:%M:%S')
                _ts = int(mktime(_ts)) + _tms
            else:
                _ts = time()
        else:
            _ts = time()
        if rules == 'S':
            return int(_ts)
        if rules == 'MS':
            return int(_ts*1000)
        return _ts

    @staticmethod
    def now_str(data=None, rules=None):
        if rules:
            rules = str(rules).upper()
        try:
            _ts = float(data)
        except Exception as e:
            _ = e
            _ts = time()
        _str = strftime("%Y-%m-%d %H:%M:%S", localtime(_ts))
        if rules == 'S':
            return _str
        if rules == 'MS':
            _str += '.%03d ' % (int(_ts * 1000) % 1000)
            return _str
        if rules == 'DATE':
            return _str.split(' ')[0]
        if rules == 'TIME':
            return _str.split(' ')[1]
        return _str


if __name__ == '__main__':
    t = Time()
    print(t.now())
    print(t.now(rules='S'))
    print(t.now(rules='MS'))
    print(t.now('2020-01-20 12:22:11'))
    print(t.now('2020-01-20 12:22:11.123'))
    print(t.now('2020-01-20 12:22:11.123', 'S'))
