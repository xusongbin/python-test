#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import strftime, localtime


class ParseFile(object):
    def __init__(self):
        pass

    @staticmethod
    def parse_time(_time, _idx, _len, _skip):
        # 起始时间：2019-12-16 09:35:00
        # 起始时间戳_calc_ts：1576460100，起始同花顺时间：0x077C8263， 同花顺每天相差：0x800
        # 计算相对于以上时间，经过了day天，当天经过了min分钟
        # 每天时间戳为86400秒，当前时间戳为：1576460100+day*86400+min*60
        _calc_index = int((_idx-_skip) / _len) % 48     # 每天第几个数据，从9点半起始
        _calc_ts = 1576460100               # 16号起始时间戳
        _calc_hex = 0x077C8263              # 16号起始位置
        _calc_step = 0x800                  # 每天的位置偏移量
        _this_hex = _time                   # 当天的位置信息
        _calc_day = 0
        _calc_min = 0
        if _calc_hex > _this_hex:
            # 当前日期在参考日期之前
            _calc_day -= int((_calc_hex - _this_hex) / _calc_step)
            _calc_min = (_calc_hex - _this_hex) % _calc_step
            if _calc_min > 0:
                _calc_day -= 1
        else:
            # 当前日期在参考日期之后
            _calc_day = int((_this_hex - _calc_hex) / _calc_step)
            _calc_min = (_this_hex - _calc_hex) % _calc_step
        _calc_now_ts = _calc_ts + _calc_day * 24 * 3600     # xxxx-xx-xx 09:35:00 当天9点35分时间戳
        # 计算当前的时间戳
        if _calc_index < 24:
            _out_ts = _calc_now_ts + _calc_index * 5 * 60
        else:
            _out_ts = _calc_now_ts + _calc_index * 5 * 60 + 1.5 * 3600
        return _out_ts

    def parse_file(self, file, digit=2):
        print(file)
        with open(file, 'rb') as f:
            byte_array = f.read()
        if not byte_array:
            return False
        _file_len = len(byte_array)
        _identify = byte_array[0:6].decode()
        _record_num = int.from_bytes(byte_array[6:10], byteorder='little')
        _record_start = int.from_bytes(byte_array[10:12], byteorder='little')
        _record_len = int.from_bytes(byte_array[12:14], byteorder='little')
        _column_num = int.from_bytes(byte_array[14:16], byteorder='little')
        print('total:{} {} num:{} start:{} len:{} column:{}'.format(
            _file_len, _identify, _record_num, _record_start, _record_len, _column_num
        ))
        # for i in range(16, _record_start, 4):
        #     print('{}\t{}'.format(i, int.from_bytes(byte_array[i:i+2], byteorder='little')))
        # return
        _column_data = byte_array[_record_start:]
        _column_per = int(_record_len/_column_num)

        _skip = True
        _skip_num = 0
        for i in range(0, _file_len - _record_start, _record_len):
            _time = int.from_bytes(_column_data[i+0:i+4], byteorder='little')
            _open = int.from_bytes(_column_data[i+4:i+8], byteorder='little')
            _high = int.from_bytes(_column_data[i+8:i+12], byteorder='little')
            _low = int.from_bytes(_column_data[i+12:i+16], byteorder='little')
            _close = int.from_bytes(_column_data[i+16:i+20], byteorder='little')
            _value = int.from_bytes(_column_data[i+20:i+24], byteorder='little')
            _volume = int.from_bytes(_column_data[i+24:i+28], byteorder='little')
            # skip
            if _skip and (abs(_time - 0x077C8263) % 0x800):
                continue
            if _skip:
                _skip = False
                _skip_num = i
            # parse
            # 计算时间点
            _time_ts = self.parse_time(_time, i, _record_len, _skip_num)
            _time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(_time_ts))
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
            # print('{} open:{:8X} high:{:8X} low:{:8X} close:{:8X} value:{:8X} volume:{:8X}'.format(
            #     _time_str, _open, _high, _low, _close, _value, _volume
            # ))

    def parse_1a0001(self):
        _file_name = r'C:\同花顺软件\同花顺\history\shase\min5\1A0001.mn5'
        self.parse_file(_file_name, 2)

    def parse_881155(self):
        _file_name = r'C:\同花顺软件\同花顺\history\newindx\min5\881155.mn5'
        self.parse_file(_file_name, 3)

    def parse_usdcnh(self):
        _file_name = r'C:\同花顺软件\同花顺\history\foreign\min5\USDCNH.mn5'
        self.parse_file(_file_name, 5)


if __name__ == '__main__':
    fp = ParseFile()
    fp.parse_1a0001()
    # fp.parse_881155()
    # fp.parse_usdcnh()
