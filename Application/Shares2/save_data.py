#!/usr/bin/env python
# -*- coding: utf-8 -*-

from my_driver import *

shares_database = 'shares.db'
shares_usdcnh_table = 'USDCNH'
shares_sh000001_table = 'SH000001'
shares_ths881155_table = 'THS881155'
shares_north_table = 'NORTH'
shares_item = 'DAY,OPEN,HIGH,LOW,CLOSE,VALUE,VOLUME'
shares_form = \
    ('(DAY DATETIME PRIMARY KEY,'
     'OPEN DOUBLE,HIGH DOUBLE,LOW DOUBLE,CLOSE DOUBLE,'
     'VALUE DOUBLE,VOLUME DOUBLE);')


class Data(object):
    def __init__(self):
        self.__sql = SQLite3(shares_database)
        self.__table_check()

    def __table_check(self):
        if not self.__sql.exist(shares_sh000001_table):
            self.__sql.create('TABLE', shares_sh000001_table, shares_form)
        if not self.__sql.exist(shares_ths881155_table):
            self.__sql.create('TABLE', shares_ths881155_table, shares_form)
        if not self.__sql.exist(shares_usdcnh_table):
            self.__sql.create('TABLE', shares_usdcnh_table, shares_form)
        if not self.__sql.exist(shares_north_table):
            self.__sql.create('TABLE', shares_north_table, shares_form)

    def __mintime(self, table, dayonly=False):
        _datetime = None
        try:
            _datetime = self.__sql.select(table, 'MIN(TIME)')[0][0]
        except Exception as e:
            _ = e
        if not _datetime:
            _datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        if dayonly:
            return _datetime.split(' ')[0]
        return _datetime

    def __maxtime(self, table, dayonly=False):
        _datetime = None
        try:
            _datetime = self.__sql.select(table, 'MAX(TIME)')[0][0]
        except Exception as e:
            _ = e
        if not _datetime:
            _datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        if dayonly:
            return _datetime.split(' ')[0]
        return _datetime

    def commit(self):
        self.__sql.commit()

    def save(self, table, day, open, high, low, close=0, value=0, volume=0):
        _val = '"{}"'.format(day)
        _val += ',{}'.format(open)
        _val += ',{}'.format(high)
        _val += ',{}'.format(low)
        _val += ',{}'.format(close)
        _val += ',{}'.format(value)
        _val += ',{}'.format(volume)
        self.__sql.replace(table, shares_item, _val)

    def select(self, table, start=None, stop=None):
        if not start:
            start = self.__mintime(table)
        if not stop:
            stop = self.__maxtime(table)
        _rule = 'TIME between "{}" and "{}"'.format(start, stop)
        return self.__sql.select(table, shares_item, _rule)


def main():
    dat = Data()
    dat.save(shares_sh000001_table, '2020-2-28 10:50:15', 1.1, 2.2, 3.3, 4.4, 5, 6)
    dat.commit()


if __name__ == '__main__':
    main()

