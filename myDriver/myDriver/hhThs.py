#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import pandas as pd
from time import time, mktime, strptime, strftime, localtime
from traceback import format_exc

from myDriver.hhLog import write_log


class Ths(object):

    def __init__(self):
        pass

    @staticmethod
    def parse_time(_time):
        _year = (_time & 0xFFF00000) >> 20
        _month = (_time & 0x000F0000) >> 16
        _day = (_time & 0x0000F800) >> 11
        _hour = (_time & 0x000007C0) >> 6
        _min = (_time & 0x0000003F) >> 0
        return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(_year+1900, _month, _day, _hour, _min, 0)

    @staticmethod
    def check_date(data_time='2020-02-27 11:30:00'):
        _now_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        if _now_time.split(' ')[0] != data_time.split(' ')[0]:
            # Not today
            return True
        _today = strftime("%Y-%m-%d 00:00:00", localtime())
        _now_day_ts = int(time() - int(mktime(strptime(_today, '%Y-%m-%d %H:%M:%S'))))
        if _now_day_ts < 32975 or _now_day_ts >= 54000 or 41400 <= _now_day_ts < 46800:
            # Closed market
            return True
        else:
            # Open market
            _ts_5min = int((time()) / 300) * 300
            _now_time = strftime("%Y-%m-%d %H:%M:%S", localtime(_ts_5min))
            if _now_time == data_time:
                return True
            _data_ts = int(mktime(strptime(data_time, '%Y-%m-%d %H:%M:%S')))
            if (time() - _data_ts) > 300:
                return True
        return False

    def parse_file(self, file, num=10000, digit=2):
        with open(file, 'rb') as f:
            byte_array = f.read()
        if not byte_array:
            return False
        write_log('Parse ')
        _total_len = len(byte_array)
        # _identify = byte_array[0:6].decode()
        _record_num = int.from_bytes(byte_array[6:10], byteorder='little')
        _record_start = int.from_bytes(byte_array[10:12], byteorder='little')
        _record_len = int.from_bytes(byte_array[12:14], byteorder='little')
        # _column_num = int.from_bytes(byte_array[14:16], byteorder='little')

        _data_array = byte_array[_record_start:]
        _data_len = len(_data_array)
        if num > _record_num:
            _num_get = _record_num
        else:
            _num_get = num
        _idx_stop = _total_len - _record_start
        _idx_start = _data_len - _num_get * _record_len
        _idx_step = _record_len

        _data_list = []
        for i in range(_idx_start, _idx_stop, _idx_step):
            _time = int.from_bytes(_data_array[i+0:i+4], byteorder='little')
            _open = int.from_bytes(_data_array[i+4:i+8], byteorder='little')
            _high = int.from_bytes(_data_array[i+8:i+12], byteorder='little')
            _low = int.from_bytes(_data_array[i+12:i+16], byteorder='little')
            _close = int.from_bytes(_data_array[i+16:i+20], byteorder='little')
            _value = int.from_bytes(_data_array[i+20:i+24], byteorder='little')
            _volume = int.from_bytes(_data_array[i+24:i+28], byteorder='little')
            # parse
            # 计算时间点
            _time_str = self.parse_time(_time)
            # TODO: maybe more than 0xC0000000
            _out_open = (_open & 0x0FFFFFFF) * pow(10, 8 - (_open >> 28))
            _out_high = (_high & 0x0FFFFFFF) * pow(10, 8 - (_high >> 28))
            _out_low = (_low & 0x0FFFFFFF) * pow(10, 8 - (_low >> 28))
            _out_close = (_close & 0x0FFFFFFF) * pow(10, 8 - (_close >> 28))
            # TODO: maybe more than 0x20000000
            _value = 0 if _value == 0xFFFFFFFF else _value
            _out_value = int((_value & 0x0FFFFFFF) * pow(10, (_value >> 28)))
            # TODO: maybe more than 0x10000000
            _volume = 0 if _volume == 0xFFFFFFFF else _volume
            _out_volume = int((_volume & 0x0FFFFFFF) * pow(10, (_volume >> 28) - 2))
            _show_str = '{} open:{:.%df} high:{:.%df} low:{:.%df} close:{:.%df} value:{} volume:{}' % (
                digit, digit, digit, digit
            )
            print(_show_str.format(_time_str, _out_open, _out_high, _out_low, _out_close, _out_value, _out_volume))
            _data_list.append([_time_str, _out_open, _out_high, _out_low, _out_close, _out_value, _out_volume])
            # print('{} open:{:8X} high:{:8X} low:{:8X} close:{:8X} value:{:8X} volume:{:8X}'.format(
            #     _time_str, _open, _high, _low, _close, _value, _volume
            # ))
        return np.array(_data_list)

    def parse_30min(self, file):
        cur = self.parse_file(file)
        next = []
        this = ['', 0, 0, 10000000, 0, 0, 0]
        for line in cur:
            if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:(05|35):\d{2}', line[0]):
                this = ['', 0, 0, 10000000, 0, 0, 0]
                this[1] = float(line[1])   # open
            this[0] = line[0]       # time
            if float(line[2]) > this[2]:   # high
                this[2] = float(line[2])
            if float(line[3]) < this[3]:   # low
                this[3] = float(line[3])
            this[5] += float(line[5])      # value
            this[6] += float(line[6])      # volume
            if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:(30|00):\d{2}', line[0]):
                this[4] = float(line[4])   # close
                next.append(this)
        return next


def div(x, y):
    return str(int(int(x)/(10000 ** y)))


if __name__ == '__main__':
    fp = Ths()
    # f = fp.parse_file(r'C:\同花顺软件\同花顺\history\shase\min5\1A0001.mn5')
    # f = fp.parse_file(r'C:\同花顺软件\同花顺\history\newindx\min5\881155.mn5')
    # f = fp.parse_file(r'C:\同花顺软件\同花顺\history\sznse\min5\399001.mn5')

    # f = fp.parse_30min(r'C:\同花顺软件\同花顺\history\shase\min5\1A0001.mn5')
    f = fp.parse_30min(r'C:\同花顺软件\同花顺\history\sznse\min5\399001.mn5')

    df = pd.DataFrame(f, columns=['时间', 'open', 'high', 'low', 'close', 'value', 'volume'])
    # del df['open']
    # del df['high']
    # del df['low']
    # del df['close']
    # del df['value']
    # df['volume'] = df['volume'].apply(div)
    # del df['open']
    # del df['high']
    # del df['low']
    # del df['close']
    # del df['volume']
    df['value'] = df['value'].apply(div, args=(2,))
    df.to_excel(r'C:\Users\Administrator\Desktop\深证30分钟.xls')
